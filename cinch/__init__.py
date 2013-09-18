
from os import environ, path
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
    def setup(cls):
        """Process any methods on this class with the name ``_setup__foo``."""
        super(Base, cls).setup()
        for name in dir(cls):
            if name.startswith('_setup__'):
                getattr(cls, name)()

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
        if hasattr(cls, 'DATABASES'):
            return
        db_user = cls.DB_USER if hasattr(cls, 'DB_USER') else cls.PROJECT_NAME
        db_type = getattr(cls, 'DATABASE_TYPE', 'sqlite')
        db_suffix = getattr(cls, 'DATABASE_SUFFIX', '_default')
        db_name = getattr(cls, 'DATABASE_NAME', cls.PROJECT_NAME + db_suffix)
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
                'NAME': path.join(DB_DIR, db_name),
            }
        else:
            raise ImproperlyConfigured("Unknown DATABASE_TYPE: {}".format(db_type))


class FHSDirsMixin(object):
    @classmethod
    def setup(cls):
        cls.LIB_DIR = join(cls.BASE_DIR, 'lib')
        cls.VAR_DIR = join(cls.BASE_DIR, 'var')
        cls.ETC_DIR = join(cls.BASE_DIR, 'etc')
        cls.SRC_DIR = join(cls.BASE_DIR, 'src')
        cls.DB_DIR = join(cls.VAR_DIR, 'db')
        cls.LOG_DIR = join(cls.VAR_DIR, 'log')

        if not hasattr(cls, 'MEDIA_ROOT'):
            cls.MEDIA_ROOT = path.join(cls.VAR_DIR, 'media')
        if not hasattr(cls, 'STATIC_ROOT'):
            cls.MEDIA_ROOT = path.join(cls.VAR_DIR, 'static')

        super(FHSDirsMixin, cls).setup()


class EnvSettingsMixin(object):

    

    @classmethod
    def setup(cls):
        """
        Set environment variables listed in ``ENV_SETTINGS`` on this
        configuration class.
        """
        try:
            env_vars = cls.ENV_SETTINGS
        except AttributeError:
            raise ImproperlyConfigured("EnvSettingsMixin requires an ENV_SETTINGS iterable.")
        for var in env_vars:
            setattr(cls, var, environ[var])
        super(EnvSettingsMixin, cls).setup()


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
        # Host routing. https://django-hosts.readthedocs.org/en/latest/
        ROOT_HOSTCONF = cls.PROJECT_NAME + '.hosts'
        DEFAULT_HOST = 'main'
        ROOT_URLCONF = cls.PROJECT_NAME + '.urls._default'
        # Let project.urls._global include project.urls._debug if it exists
        if not hasattr(cls, 'DEBUG_URLPATTERNS_ENABLED'):
            cls.DEBUG_URLPATTERNS_ENABLED = cls.DEBUG

        if cls.DEBUG:
            debug_hosts = []
            for host in cls.ALLOWED_HOSTS:
                if any(part for part in host.split('.') if not part.isdigit()):
                    debug_hosts.append(host + '.local')

        super(HostsMixin, cls).setup()
