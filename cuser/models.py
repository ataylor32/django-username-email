from typing import TYPE_CHECKING, Any, ClassVar, Optional, TypeVar, Union

from django.db import models
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, PermissionsMixin, AbstractBaseUser
)
from django.contrib.auth.models import Group as BaseGroup
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    import datetime

    from django.contrib.auth.models import Permission
    from django.db.models import QuerySet
    from django.db.models.expressions import Combinable
    from django_stubs_ext import StrOrPromise
    from typing_extensions import Self

_UserT = TypeVar('_UserT', bound='AbstractCUser')


class CUserManager(BaseUserManager[_UserT]):
    use_in_migrations = True

    def _create_user(self, email: str, password: Optional[str], **extra_fields: Any) -> _UserT:
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> _UserT:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> _UserT:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(
        self,
        perm: Union[str, 'Permission'],
        is_active: bool = True,
        include_superusers: bool = True,
        backend: Optional[str] = None,
        obj: Optional[models.Model] = None,
    ) -> 'QuerySet[_UserT]':
        backend_obj: Any
        if backend is None:
            backends = auth._get_backends(return_tuples=True)  # type: ignore[attr-defined]  # pylint: disable=protected-access
            if len(backends) == 1:
                backend_obj, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend_obj = auth.load_backend(backend)
        if hasattr(backend_obj, 'with_perm'):
            queryset: 'QuerySet[_UserT]' = backend_obj.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
            return queryset
        return self.none()


class AbstractCUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    email: 'models.EmailField[Union[str, Combinable], str]' = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    first_name: 'models.CharField[Union[str, int, Combinable], str]' = models.CharField(
        _('first name'), max_length=150, blank=True
    )
    last_name: 'models.CharField[Union[str, int, Combinable], str]' = models.CharField(
        _('last name'), max_length=150, blank=True
    )
    is_staff: 'models.BooleanField[Union[bool, Combinable], bool]' = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined: (
        'models.DateTimeField[Union[str, datetime.datetime, datetime.date, Combinable], datetime.datetime]'
    ) = models.DateTimeField(_('date joined'), default=timezone.now)

    objects: ClassVar['CUserManager[Self]'] = CUserManager()  # pyright: ignore [reportIncompatibleVariableOverride]

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name

    def email_user(
        self,
        subject: 'StrOrPromise',
        message: 'StrOrPromise',
        from_email: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class CUser(AbstractCUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Password and email are required. Other fields are optional.
    """
    class Meta(AbstractCUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Group(BaseGroup):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True
