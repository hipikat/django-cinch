
from os import environ
import sys
from django.core.exceptions import ImproperlyConfigured


def cinch_django_settings(settings_globals=None, env_var='DJANGO_SETTINGS_CLASS'):
    settings_obj = settings_globals[environ[env_var]]()
    settings = {att: getattr(settings_obj, att)
                for att in dir(settings_obj)
                if att == att.upper()}
    settings_globals.update(settings)


class CinchSettings(object):
    """
    Base class for settings classes. TODOLipsum
    """

    # Names of attributes which have only been set with CinchSettings.setdefault()
    _defaults = set()

    def __init__(self, *args, **kwargs):
        super(CinchSettings, self).__init__(*args, **kwargs)
        self.setup()

    def __setattribute__(self, name, value):
        """
        Set an attribute on the class, removing its name from the set of attributes
        which have been attached to the class using CinchSettings.setdefault().
        """
        # If this attribute was previously set with setdefault(), we can safely
        # discard it from the set of _defaults. If it hasn't, setdefault() will
        # add it to that set in the extremely near future.
        self._defaults.discard(name)
        super(CinchSettings, self).__setattribute__(name, value)

    def explicit(self, name):
        """
        Return True if the attribute ``name`` has been explicitely set on this
        class, i.e. not with setdefault(). Otherwise, return False.
        """
        return True if hasattr(self, name) and name not in self._defaults else False

    def setdefault(self, key, *default):
        """
        If ``key`` is an attribute of this instance, return its value. If not,
        set the attribute ``key`` to ``default[0]`` and return its value. If a
        default is not passed and ``key`` is not an attribute on the instance,
        an ``AttributeError`` is raised.
        """
        if len(default) > 1:
            raise TypeError("{}.setdefault takes 0 or 1 argument ({} given)".format(
                self.__class__.__name__, len(default)))
        try:
            return getattr(self, key)
        except AttributeError:
            if default:
                setattr(self, key, default[0])
                self._defaults.add(key)
                return default[0]
            raise

    def setup(cnf, *args, **kwargs):
        """Do nothing; CinchSettings should always be the final base class."""


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
        cnf.setdefault('INTERNAL_IPS', tuple('127.0.0.1'))

        # URLs
        cnf.setdefault('STATIC_URL', '/static/')
        cnf.setdefault('MEDIA_URL', '/media/')
        if hasattr(cnf, 'PROJECT_MODULE'):
            cnf.setdefault('ROOT_URLCONF', cnf.PROJECT_MODULE + '.urls')

        super(NormaliseSettings, cnf).setup(*args, **kwargs)

# Weak i18n :)
NormalizeSettings = NormaliseSettings
