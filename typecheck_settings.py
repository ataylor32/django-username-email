# Minimal Django settings used by the django-stubs mypy plugin when type
# checking (see mypy.ini and the "typecheck" environment in tox.ini).
SECRET_KEY = 'typecheck'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cuser',
]
AUTH_USER_MODEL = 'cuser.CUser'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
USE_TZ = True
