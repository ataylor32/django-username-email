CUser, make email the USERNAME\_FIELD
=====================================

CUser makes it easy to use email address as your identification token
instead of a username.

CUser is a custom Django user model (extends ``AbstractBaseUser``) so it
takes a tiny amount of effort to use.

The only difference between CUser and the vanilla Django ``User`` is email
address is the ``USERNAME_FIELD`` (and username does not exist).

CUser supports Django 1.11+. If you need to use CUser with Django 1.8 - Django
1.10, you must install an older, unmaintained version of CUser, as noted in the
"Install & Set up" section.

Why use CUser?
--------------

Because you want everything in ``django.contrib.auth`` except for the
``username`` field and you also want users to **log in with email addresses**.
And you don't want to create your own custom user model or authentication
backend.

Install & Set up
----------------

0. If you previously used Django's default user model,
   ``django.contrib.auth.models.User``, jump to **Notes** first (then come
   back). Otherwise, continue onward!

1. Install with ``pip``:

   .. code-block:: shell

       # Django 2.0
       pip install django-username-email

       # Django 1.11
       pip install "django-username-email<2.2"

       # Django 1.8 - Django 1.10 (unmaintained)
       pip install django-username-email==2.1.2

2. Add ``cuser`` to your ``INSTALLED_APPS`` setting:

   .. code-block:: python

       INSTALLED_APPS = [
           ...
           'cuser',
       ]

3. Specify the custom model as the default user model for your project
   using the ``AUTH_USER_MODEL`` setting in your settings.py:

   .. code-block:: python

       AUTH_USER_MODEL = 'cuser.CUser'

4. Instead of referring to User directly, you should reference the user
   model using ``django.contrib.auth.get_user_model()``

5. If you use Django's default ``AuthenticationForm`` class, it is
   strongly recommended that you replace it with the one included with
   CUser. This will make the ``<input>`` have its ``type`` attribute set
   to ``email`` and browsers' autocomplete feature will suggest email
   addresses instead of usernames. For example, if your project is using
   Django's default ``login`` view (or ``LoginView`` in Django 1.11+), this is
   what you would put in your urls.py in order to make use of CUser's
   ``AuthenticationForm`` class:

   .. code-block:: python

       from cuser.forms import AuthenticationForm
       from django.conf.urls import include, url
       from django.contrib.auth.views import login

       urlpatterns = [
           url(r'^accounts/login/$', login, {'authentication_form': AuthenticationForm}, name='login'),
           url(r'^accounts/', include('django.contrib.auth.urls')),
           ...
       ]

   Or if you're using Django 1.11+:

   .. code-block:: python

       from cuser.forms import AuthenticationForm
       from django.conf.urls import include, url
       from django.contrib.auth.views import LoginView

       urlpatterns = [
           url(r'^accounts/login/$', LoginView.as_view(authentication_form=AuthenticationForm), name='login'),
           url(r'^accounts/', include('django.contrib.auth.urls')),
           ...
       ]

6. Run migrations.

   .. code-block:: shell

       python manage.py migrate

7. There is a good chance that you want foo@example.com and FOO@example.com to
   be treated as the same email address. There is a variety of ways to go about
   doing this. How you handle it will depend on the needs of your project and
   personal preference, so CUser does not provide a solution for this out of
   the box. You will need to address this yourself if this applies to you.

Configuration
-------------

To override any of the default settings, create a dictionary named ``CUSER`` in
your settings.py with each setting you want to override. For example:

.. code-block:: python

    CUSER = {
        'app_verbose_name': 'Authentication and Authorization',
        'register_proxy_auth_group_model': True,
    }

These are the settings:

``app_verbose_name`` (default: ``_("Custom User")``)
****************************************************

This controls the value that CUser will use for its ``AppConfig`` class'
``verbose_name``.

``register_proxy_auth_group_model`` (default: ``False``)
********************************************************

When set to ``True``, CUser's admin.py will unregister Django's default
``Group`` model and register its own proxy model of Django's default ``Group``
model (also named ``Group``). This is useful if you want Django's default
``Group`` model to appear in the same part of the admin as CUser's ``CUser``
model.

Change default table name
-------------------------

By default Django gives the default table name in data base for each model.
In our case it is equal to ``cuser_cuser``. If you want to change it you need
to add ``db_table`` value to ``CUSER`` dictionary in your settings file.
For instance, when you add:

.. code-block:: python

    CUSER = {
        ...
        'db_table': 'users',
    }

And run  the following after that:

.. code-block:: shell

       python manage.py makemigrations cuser
       python manage.py migrate

your table name for custom user model will be equal to ``users``

Notes
-----

If you have tables referencing Django's ``User`` model, you will have to
delete those table and migrations, then re-migrate. This will ensure
everything is set up correctly from the beginning.

When you define a foreign key or many-to-many relations to the ``User``
model, you should specify the custom model using the ``AUTH_USER_MODEL``
setting.

For example:

.. code-block:: python

    from django.conf import settings
    from django.db import models

    class Profile(models.Model):
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
    )

License
-------

Released under the MIT license. See LICENSE for details.

Questions, comments, or anything else?
--------------------------------------

-  Open an issue
-  `Twitter <https://twitter.com/tomfme>`__
-  tom@meagher.co
