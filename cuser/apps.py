from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CuserConfig(AppConfig):
    name = 'cuser'
    verbose_name = _("Custom User")
