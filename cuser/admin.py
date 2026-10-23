from typing import TYPE_CHECKING, Optional

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
    from django.contrib.admin.options import _FieldsetSpec


@admin.register(CUser)
class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/cuser/cuser/add_form.html'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    form = UserChangeForm
    add_form = AdminUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

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
