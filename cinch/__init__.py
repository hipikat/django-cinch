
from itertools import chain
from os import environ
import sys
from .mixins import SetDefaultMixin


__version__ = '0.0.1'


def cinch_settings(settings_globals, settings_class):
    settings_obj = settings_globals[settings_class]()
    settings = {att: getattr(settings_obj, att)
                for att in dir(settings_obj)
                if att == att.upper()}
    settings_globals.update(settings)


def cinch_django_settings(settings_globals, env_var='DJANGO_SETTINGS_CLASS'):
    cinch_settings(settings_globals, environ[env_var])


class CinchSettings(SetDefaultMixin):
    """
    Base class for settings classes. TODOLipsum
    """
    def __init__(self, *args, **kwargs):
        super(CinchSettings, self).__init__(*args, **kwargs)
        self.setup()

    def setup(cnf, *args, **kwargs):
        """
        Do nothing, for now. CinchSettings should always be the final
        class in the list of ``bases``.
        """


# TODO: Sub-class from FileLoggingMixin in .logging? (at least?)
class NormaliseSettings(object):
    """
    Mixin to set sensible defaults on a CinchSettings class. TODOLipsum
    """
    __missing_setting_msg = "Attribute {} must be set on a class instance "\
        "which includes the NormaliseSettings mixin in its bases."

    def setup(cnf, *args, **kwargs):
        """Set default attributes on this class, if they haven't been set."""

        # Project metadata
        try:
            cnf.setdefault('MANAGERS', cnf.ADMINS)
        except AttributeError:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(cnf.__missing_setting_msg.format('ADMINS'))
        cnf.setdefault('TIME_ZONE', 'UTC')      # Default is "America/Chicago"
        cnf.setdefault('LANGUAGE_CODE', 'en')   # Default is 'en-us'
        cnf.setdefault('SITE_ID', 1)            # Default is not defined
        cnf.setdefault('WSGI_APPLICATION', cnf.PROJECT_MODULE + '.wsgi.application')

        # Debugging, testing, development
        cnf.setdefault('DEBUG', False)
        cnf.setdefault('TEMPLATE_DEBUG', cnf.DEBUG)
        cnf.setdefault('TESTING', True if 'test' in sys.argv else False)

        # Security
        cnf.setdefault('INTERNAL_IPS', ('127.0.0.1',))
        if cnf.DEBUG and hasattr(cnf, 'ALLOWED_HOSTS'):
            local_hosts = [host + '.local' for host in cnf.ALLOWED_HOSTS if host[0] == '.']
            cnf.ALLOWED_HOSTS = list(chain(cnf.ALLOWED_HOSTS, local_hosts))

        # URLs
        cnf.setdefault('STATIC_URL', '/static/')
        cnf.setdefault('MEDIA_URL', '/media/')
        if hasattr(cnf, 'PROJECT_MODULE'):
            cnf.setdefault('ROOT_URLCONF', cnf.PROJECT_MODULE + '.urls')

        super(NormaliseSettings, cnf).setup(*args, **kwargs)

# Weak i18n :)
NormalizeSettings = NormaliseSettings
