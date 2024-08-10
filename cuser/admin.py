import django
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as StockGroup
from django.utils.translation import gettext_lazy as _

from cuser.forms import UserChangeForm, UserCreationForm
from cuser.models import CUser, Group
from cuser.settings import CUSER_SETTINGS


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
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            add_fieldsets = (
                (None, {
                    'classes': ('wide',),
                    'fields': ['email', 'password1', 'password2'],
                }),
            )

            if django.VERSION >= (5, 1):
                add_fieldsets[0][1]['fields'].insert(1, 'usable_password')

            return add_fieldsets

        return super().get_fieldsets(request, obj)


if CUSER_SETTINGS['register_proxy_auth_group_model']:
    admin.site.unregister(StockGroup)

    @admin.register(Group)
    class GroupAdmin(BaseGroupAdmin):
        pass
