
from os import path


class SetDefaultMixin(object):
    """
    Adds ``setdefault()`` and ``explicit()`` methods to the class TODOLipsum.
    """
    # Names of attributes which have only been set with SetDefaultMixin.setdefault()
    _setdefault_defaults = set()

    def __setattribute__(self, name, value):
        """
        Set an attribute on the class, removing its name from the set of attributes
        which have been attached to the class using CinchSettings.setdefault().
        """
        # If this attribute was previously set with setdefault(), we can safely
        # discard it from the set of _defaults. If it hasn't, and the attribute
        # is being set by self.setdefault() itself, setdefault() will add its name
        # to self._setdefault_defaults right after this function.
        self._defaults.discard(name)
        super(SetDefaultMixin, self).__setattribute__(name, value)

    def explicit(self, name):
        """
        Return True if the attribute ``name`` has been explicitely set on this
        class, i.e. not with setdefault(). Otherwise, return False.
        """
        return True if hasattr(self, name) and name not in self._setdefault_defaults else False

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
                self._setdefault_defaults.add(key)
                return default[0]
            raise


class FHSDirsMixin(SetDefaultMixin):
    _fhsdirs_altered = set()

    def __setattr__(self, name, value):
        """
        Call ``self.setup()`` when PROJECT_PATH is set on the class. Also track
        attributes which have been set since ``self.setup()`` was last called.
        """
        super(FHSDirsMixin, self).__setattr__('_fhsdirs_altered',
                                              self._fhsdirs_altered | set(['name']))
        super(FHSDirsMixin, self).__setattr__(name, value)
        if name == 'PROJECT_PATH':
            self.setup()

    def setup(self, *args, **kwargs):
        """
        Set a complement of FHS-style directory attribute values on this
        object, if they haven't already been explicitely set, or if the
        keyword argument value ``force`` is ``True``.
        """
        # If called from a class (such as `CinchSettings`) being
        # instantitated, it's easier to set PROJECT_PATH on the sub-class.
        if 'project_path' in kwargs:
            self.PROJECT_PATH = kwargs['project_path']
        
        kwargs['force'] = kwargs.get('force', False)

        #@staticmethod
        def set_default(name, val):
            # Only setdefault() on self if the directory hasn't been
            # explicitly set, or setup(force=True).
            if name not in self._fhsdirs_altered or kwargs['force']:
                self.setdefault(name, val)

        set_default('ETC_DIR', path.join(self.PROJECT_PATH, 'etc'))               # etc/
        set_default('ETC_LOCAL_DIR', path.join(self.ETC_DIR, 'local'))         # etc/local/
        set_default('LIB_DIR', path.join(self.PROJECT_PATH, 'lib'))               # lib/
        set_default('SRC_DIR', path.join(self.PROJECT_PATH, 'src'))               # src/
        set_default('TEMPLATE_DIRS', [path.join(self.SRC_DIR, 'templates')])  # src/templates/
        set_default('USR_DIR', path.join(self.PROJECT_PATH, 'src'))               # src/
        set_default('VAR_DIR', path.join(self.PROJECT_PATH, 'var'))               # var/
        #set_default('ENV_DIR', path.join(self.VAR_DIR, 'var', 'env'))        # var/env
        set_default('DB_DIR', path.join(self.VAR_DIR, 'db'))                  # var/db/
        set_default('FIXTURES_DIRS', [path.join(self.VAR_DIR, 'fixtures')])   # var/fixtures/
        set_default('LOG_DIR', path.join(self.VAR_DIR, 'log'))                # var/log/
        set_default('MEDIA_ROOT', path.join(self.VAR_DIR, 'media'))           # var/media/
        set_default('STATIC_ROOT', path.join(self.VAR_DIR, 'static'))         # var/static/

        self._fhsdirs_altered = set()
        sup = super(FHSDirsMixin, self)
        if hasattr(sup, 'setup'):
            sup.setup(*args, **kwargs)


#def fhs_dirs(project_path):
#    class FHSDirs(FHSDirsMixin):
#        PROJECT_PATH = project_path
#    return FHSDirs(project_path)


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
