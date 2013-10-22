
from os import environ, path
import sys
from django.core.exceptions import ImproperlyConfigured
#from configurations import Configuration


def cinch_django_settings(settings_globals=None, env_var='DJANGO_SETTINGS_CLASS'):
    settings_class = settings_globals[environ[env_var]]
    settings = {att: getattr(settings_class, att)
                for att in dir(settings_class())
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
        cnf.setdefault('WSGI_APPLICATION', cnf.PROJECT_MODULE + '.urls')

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

        # Logging
        cnf.setdefault('LOGGING', {
            'formatters': {
                'verbose': {
                    'format': "\n%(levelname)s [%(asctime)s][%(pathname)s:%(lineno)s]" +
                              "[p/t:%(process)d/%(thread)d]\n%(message)s"
                },
                'simple': {
                    'format': '%(levelname)s [%(module)s:%(lineno)s] %(message)s'
                },
            },
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                },
            },
            'handlers': {
                'mail_admins': {
                    'level': 'ERROR',
                    'filters': ['require_debug_false'],
                    'class': 'django.utils.log.AdminEmailHandler',
                },
            },
            'loggers': {
                'django.request': {
                    'handlers': ['mail_admins'],
                    'level': 'ERROR',
                    'propagate': True,
                },
            },
        })

        super(NormaliseSettings, cnf).setup(*args, **kwargs)

# Weak i18n :)
NormalizeSettings = NormaliseSettings


class FHSDirsMixin(object):
    @classmethod
    def setup(cnf, *args, **kwargs):
        cnf.setdefault('ETC_DIR', path.join(cnf.BASE_DIR, 'etc'))               # etc/
        cnf.setdefault('LIB_DIR', path.join(cnf.BASE_DIR, 'lib'))               # lib/
        cnf.setdefault('SRC_DIR', path.join(cnf.BASE_DIR, 'src'))               # src/
        cnf.setdefault('TEMPLATE_DIRS', [path.join(cnf.SRC_DIR, 'templates')])  # src/templates/
        cnf.setdefault('VAR_DIR', path.join(cnf.BASE_DIR, 'var'))               # var/
        cnf.setdefault('DB_DIR', path.join(cnf.VAR_DIR, 'db'))                  # var/db/
        cnf.setdefault('FIXTURES_DIRS', [path.join(cnf.VAR_DIR, 'fixtures')])   # var/fixtures/
        cnf.setdefault('LOG_DIR', path.join(cnf.VAR_DIR, 'log'))                # var/log/
        cnf.setdefault('MEDIA_ROOT', path.join(cnf.VAR_DIR, 'media'))           # var/media/
        cnf.setdefault('STATIC_ROOT', path.join(cnf.VAR_DIR, 'static'))         # var/static/

        super(FHSDirsMixin, cnf).setup(*args, **kwargs)


#class DjangoHostsURLsMixin(object):
#    """
#    Standardised configuration for django-hosts. To use it, a configuration
#    class must set PROJECT_NAME, todolipsum...
#
#    This mixin sets the ``ROOT_HOSTCONF`` to ``PROJECT_NAME.hosts``, todolipsum
#    -
#    loaded from a PROJECT_NAME.
#    --
#    If ``DEBUG`` is True, for each host 'foo.bar' in ``ALLOWED_HOSTS`` add
#    a host 'foo.bar.local', for easier local development.
#    """
#    @classmethod
#    def setup(cnf, *args, **kwargs):
#        super(DjangoHostsURLsMixin, cnf).setup(*args, **kwargs)
#
#        # Host routing with django-hosts - https://django-hosts.readthedocs.org/en/latest/
#        cls.ROOT_HOSTCONF = cls.PROJECT_NAME + '.hosts'
#        cls.DEFAULT_HOST = 'main'
#
#        # Fallback/default url conf
#        cls.ROOT_URLCONF = cls.PROJECT_NAME + '.urls._default'
#
#        # Let project.urls._global include project.urls._debug if it exists
#        if not hasattr(cls, 'DEBUG_URLPATTERNS_ENABLED'):
#            cls.DEBUG_URLPATTERNS_ENABLED = cls.DEBUG
#
#        # Allow 'example.com.local' hosts, if debugging is turned on
#        # TODO: Argh this makes no sense as host validation only works when debug's off.
#        # Okay wait we want this here to work with django-hosts(??)
#        if cls.DEBUG:
#            debug_hosts = []
#            for host in cls.ALLOWED_HOSTS:
#                # TODO: Import something to distinguish ips from named domains.
#                if any(part for part in host.split('.') if not part.isdigit()):
#                    debug_hosts.append(host + '.local')
#
#        super(HostsURLsMixin, cls).setup()
