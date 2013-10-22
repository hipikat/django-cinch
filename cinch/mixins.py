
from os import path

class FHSDirsMixin(object):
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
