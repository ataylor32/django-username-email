from django.conf import settings
from django.utils.translation import gettext_lazy as _

CUSER_SETTINGS = {
    'app_verbose_name': _("Custom User"),
    'register_proxy_auth_group_model': False,
}

if hasattr(settings, 'CUSER'):
    CUSER_SETTINGS.update(settings.CUSER)
