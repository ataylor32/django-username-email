from django.apps import AppConfig
from .settings import CUSER_SETTINGS


class CuserConfig(AppConfig):
    name = 'cuser'
    verbose_name = CUSER_SETTINGS['app_verbose_name']
    default_auto_field = 'django.db.models.AutoField'
