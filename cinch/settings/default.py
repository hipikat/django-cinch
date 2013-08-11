"""
These are the default settings used by manage.py and the default wsgi
application instance when no DJANGO_SETTINGS_MODULE environment variable
is set. They provide the minimum configuration needed to create a
running server or invoke a Django shell. Generally, a
DJANGO_SETTINGS_MODULE environment variable should be set. The author
suggests a postactivate hook in the project's virtual environment.
"""

from revkom.settings import base_settings_mixin


ADMINS = ()
PROJECT_NAME = 'revkom'

execfile(base_settings_mixin('debug'))
