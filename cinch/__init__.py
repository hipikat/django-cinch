
from os import environ, path
import sys
from runpy import run_module
from django.core.exceptions import ImproperlyConfigured
from configurations import Configuration
from .caches import *
from .common import *
from .databases import *


def cinch_settings(globals_dict, name=None):
    if not name:
        name = 'prod' if not globals_dict.get('DEBUG') else 'debug'
    module_name = 'cinch.settings.' + name
    return run_module(module_name, globals_dict)


class BaseConfiguration(Configuration):

    @classmethod
    def _get_cinch_meta(cls, value, *default):
        """Return a named value from a configuration's CinchMeta class."""
        try:
            return getattr(cls.CinchMeta, value)
        except AttributeError:
            try:
                return default[0]
            except IndexError:
                raise AttributeError(
                    "Missing required attribute {}.CinchMeta.{}".format(cls.__name__, value))
        
    @classmethod
    def setup(cls):
        """Process any methods on this class with the name ``_setup__foo``."""
        super(BaseConfiguration, cls).setup()
        for name in dir(cls):
            if name.startswith('_setup__'):
                getattr(cls, name)()
        # TODOLipsum: set defaults
        if not hasattr(cls, 'ROOT_URLCONF'):
            cls.ROOT_URLCONF = cls.PROJECT_NAME + '.urls'
        #import pdb; pdb.set_trace()

    SITE_ID = 1

    # Debugging, development and testing
    TESTING = True if 'test' in sys.argv else False
    DEBUG = False   # Never assume o.o
    @classmethod
    def _setup__debug(cls):
        # TODO: Can we use setdefault on cls.__dict__ or something?
        if not hasattr(cls, 'TEMPLATE_DEBUG'):
            cls.TEMPLATE_DEBUG = cls.DEBUG

    INTERNAL_IPS = ('127.0.0.1',)

    # URLs
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    # Databases
    @classmethod
    def _setup__databases(cls):
        """
        If ``DATABASES`` haven't been defined, configure a default database
        based on DATABASE_TYPE, falling back to sqlite if it hasn't been set.
        Valid values for ``DATABASE_TYPE`` are 'postgresql' and 'sqlite'.
        """
        if hasattr(cls, 'DATABASES') and len(cls.DATABASES):
            return

        db_user = cls._get_cinch_meta('DATABASE_USER', cls.PROJECT_NAME)
        db_type = cls._get_cinch_meta('DATABASE_TYPE', 'sqlite')
        db_suffix = cls._get_cinch_meta('DATABASE_SUFFIX',
            '_default' if db_type != 'sqlite' else '_default.db')
        db_name = cls._get_cinch_meta('DATABASE_NAME', cls.PROJECT_NAME + db_suffix)

        cls.DATABASES = {}
        if db_type is 'postgresql':
            cls.DATABASES['default'] = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': db_name,
                'USER': db_user,
            }   

        elif db_type is 'sqlite':
            cls.DATABASES['default'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': path.join(cls.DB_DIR, db_name),
            }
        else:
            raise ImproperlyConfigured("Unknown DATABASE_TYPE: {}".format(db_type))


class FHSDirsMixin(object):
    @classmethod
    def setup(cls):
        cls.LIB_DIR = path.join(cls.BASE_DIR, 'lib')
        cls.VAR_DIR = path.join(cls.BASE_DIR, 'var')
        cls.ETC_DIR = path.join(cls.BASE_DIR, 'etc')
        cls.SRC_DIR = path.join(cls.BASE_DIR, 'src')
        cls.DB_DIR = path.join(cls.VAR_DIR, 'db')
        cls.LOG_DIR = path.join(cls.VAR_DIR, 'log')

        if not hasattr(cls, 'MEDIA_ROOT') or not len(cls.MEDIA_ROOT):
            cls.MEDIA_ROOT = path.join(cls.VAR_DIR, 'media')
        if not hasattr(cls, 'STATIC_ROOT') or not len(cls.STATIC_ROOT):
            cls.STATIC_ROOT = path.join(cls.VAR_DIR, 'static')
        if not hasattr(cls, 'TEMPLATE_DIRS') or not len(cls.TEMPLATE_DIRS):
            cls.TEMPLATE_DIRS = [path.join(cls.SRC_DIR, 'templates')]

        super(FHSDirsMixin, cls).setup()


# TODO: Delete? django-configurations has Values now.
#class EnvSettingsMixin(object):
#
#    @classmethod
#    def setup(cls):
#        """
#        Set environment variables listed in ``ENV_SETTINGS`` on this
#        configuration class.
#        """
#        try:
#            env_vars = cls._get_cinch_meta('ENV_SETTINGS')
#        except AttributeError:
#            raise ImproperlyConfigured("EnvSettingsMixin requires a CinchMeta.ENV_SETTINGS iterable.")
#        for var in env_vars:
#            setattr(cls, var, environ[var])
#        super(EnvSettingsMixin, cls).setup()


class HostsURLsMixin(object):
    """
    Standardised configuration for django-hosts. To use it, a configuration
    class must set PROJECT_NAME, todolipsum...

    This mixin sets the ``ROOT_HOSTCONF`` to ``PROJECT_NAME.hosts``, todolipsum
    - 
    loaded from a PROJECT_NAME.
    --
    If ``DEBUG`` is True, for each host 'foo.bar' in ``ALLOWED_HOSTS`` add
    a host 'foo.bar.local', for easier local development.
    """
    @classmethod
    def setup(cls):
        # Host routing, with django-hosts
        # https://django-hosts.readthedocs.org/en/latest/
        cls.ROOT_HOSTCONF = cls.PROJECT_NAME + '.hosts'
        cls.DEFAULT_HOST = 'main'

        # Fallback/default url conf
        cls.ROOT_URLCONF = cls.PROJECT_NAME + '.urls._default'

        # Let project.urls._global include project.urls._debug if it exists
        if not hasattr(cls, 'DEBUG_URLPATTERNS_ENABLED'):
            cls.DEBUG_URLPATTERNS_ENABLED = cls.DEBUG

        # Allow 'example.com.local' hosts, if debugging is turned on
        # TODO: Argh this makes no sense as host validation only works when debug's off.
        # Okay wait we want this here to work with django-hosts(??)
        if cls.DEBUG:
            debug_hosts = []
            for host in cls.ALLOWED_HOSTS:
                # TODO: Import something to distinguish ips from named domains.
                if any(part for part in host.split('.') if not part.isdigit()):
                    debug_hosts.append(host + '.local')

        super(HostsURLsMixin, cls).setup()
