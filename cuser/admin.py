from typing import TYPE_CHECKING, Any, Optional, cast

import django
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as StockGroup
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from cuser.forms import AdminUserCreationForm, UserChangeForm
from cuser.models import CUser, Group
from cuser.settings import CUSER_SETTINGS

if TYPE_CHECKING:
    from typing import Callable, Union

    from django.contrib.admin.options import _FieldsetSpec
    from django.utils.datastructures import _ListOrTuple


@admin.register(CUser)
class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/cuser/cuser/add_form.html'
    # The casts give these the types ModelAdmin declares in django-stubs.
    # Otherwise, mypy infers fixed-length tuple types, which would reject
    # subclasses that use a different number of items, a list, etc.
    # Annotations can't be used instead because django-stubs only declares
    # some of these as ClassVar in newer versions.
    fieldsets = cast('Optional[_FieldsetSpec]', (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    ))
    form = UserChangeForm
    add_form = AdminUserCreationForm
    list_display = cast(
        '_ListOrTuple[Union[str, Callable[[Any], Union[str, bool]]]]',
        ('email', 'first_name', 'last_name', 'is_staff'),
    )
    search_fields = cast('_ListOrTuple[str]', ('email', 'first_name', 'last_name'))
    # django-stubs only allows expressions here in newer versions, so this is
    # left as Any and subclasses are checked against ModelAdmin's own type.
    ordering = cast(Any, ('email',))

    def get_fieldsets(
        self, request: HttpRequest, obj: Optional[CUser] = None
    ) -> '_FieldsetSpec':
        if not obj:
            usable_password_fields = ['usable_password'] if django.VERSION >= (5, 1) else []

            return (
                (None, {
                    'classes': ('wide',),
                    'fields': ['email', *usable_password_fields, 'password1', 'password2'],
                }),
            )

        return super().get_fieldsets(request, obj)


if CUSER_SETTINGS['register_proxy_auth_group_model']:
    admin.site.unregister(StockGroup)

    @admin.register(Group)
    class GroupAdmin(BaseGroupAdmin):
        pass
