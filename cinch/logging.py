
import os
from collections import Mapping
from revkom.coll import EasyList, deep_update


###
# Logging
###
LOGGING_SETTINGS_DEFAULTS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {},
    'filters': {},
    'handlers': {},
    'loggers': {},
}
LOGFILE_DEFAULTS = {
    'level': 'DEBUG',   # Level's set by loggers, so debug here catch anything.
    'class': 'logging.handlers.RotatingFileHandler',    # Keep files,
    'backupCount': 2,                                   # up to 2,
    'maxBytes': (10 ** 7),                              # of 10 MB each.
    'formatter': 'verbose',     # Including all potentially useful information.
}


class LoggingSetting(dict):
    """
    A dictConfig manager class, for configuring logging.
    - https://docs.djangoproject.com/en/dev/topics/logging/\
        #django-s-default-logging-configuration
    - http://docs.python.org/2/library/logging.config.html
    """
    def __init__(self, *args, **kwargs):
        # Install the default keys/values, either passed in or defined above.
        self.update(
            kwargs.pop('defaults') if 'defaults' in kwargs
            else LOGGING_SETTINGS_DEFAULTS)
        # Update self with dicts passed to the constructor.
        for arg in args:
            if isinstance(arg, Mapping):
                self.deep_update(arg)
            else:
                from pprint import pprint
                pprint(arg)
                raise TypeError("Only Mappings are accepted as arguments.")
        # Set logfile defaults from a passed paramter or the defaults above.
        self.logfile_defaults = kwargs.pop('logfile_defaults') \
            if 'logfile_defaults' in kwargs else LOGFILE_DEFAULTS
        # Set the logfile_dir if one was specified.
        self.logfile_dir = kwargs.pop('logfile_dir') \
            if 'logfile_dir' in kwargs else None
        # Apply any remaining keyword arguments as attributes on self.
        for (key, val) in kwargs.iteritems():
            self[key] = val
        # We've processed all the constructor arguments, but should still let
        # the super class do any initialisation it needs to without arguments.
        super(LoggingSetting, self).__init__()

    def deep_update(self, updated):
        """
        Update nested mappings without implicitly removing missing values. I.e.:

        >>> log_conf = LoggingSetting({'loggers': {'django': 'log_conf'}})
        # deep_update() doesn't overwrite 'django' key in 'loggers' mapping
        >>> log_conf.deep_update({'loggers': {'my_app': 'bar'}})
        >>> 'my_app' in log_conf['loggers'] and 'django' in log_conf['loggers']
        True
        # Regular update() replaces 'loggers' with its own argument
        >>> log_conf.update({'loggers': {'my_app': 'bar'}})
        >>> log_conf['loggers']
        {'my_app': 'bar'}
        """
        self = deep_update(self, updated)

    def add_logfile_handler(self, handler_name=None, *prefixes, **kwargs):
        """
        Creates an '[prefix1-prefix2-...](handler_name)-logfile' logging
        handler, using LOGFILE_DEFAULTS or a passed logfile_defaults, which
        write to [prefix1.prefix2.etc.]handler_name.log, in the directory
        self.log_dir (a string to a writable directory you should set when
        initialising an instance of this class (or whenever)).
        """
        # Get the full path to a logfile to be written or die trying.
        if 'file_path' in kwargs:
            file_path = kwargs.pop('file_path')
        else:
            try:
                logfile_dir = kwargs.get('logfile_dir', self.logfile_dir)
            except KeyError:
                raise RuntimeError(
                    "A logfile_dir attribute must be set on this class or" +
                    "passed to this function as a keyword argument.")
        if logfile_dir[-1] != os.sep:
            logfile_dir += os.sep
        dot_prefix = ".".join(prefixes) + '.' if prefixes else ''
        file_path = dot_prefix + handler_name + '.log'
        # Construct a name for the handler, which is set in the logger.
        dash_prefix = "-".join(prefixes) + '-' if prefixes else ''
        handler_name = dash_prefix + handler_name + '_logfile'
        # Set the properties of the handler from known defaults and kwargs.
        self['handlers'][handler_name] = self.logfile_defaults.copy() \
            if 'defaults' not in kwargs else kwargs.pop('defaults')
        self['handlers'][handler_name]['filename'] = file_path
        # Set any remaining keywoard arguments as attributes of the handler.
        for (key, val) in kwargs.iteritems():
            self['handlers'][handler_name][key] = val

    def add_logfile_handlers_for_apps(self, *apps, **kwargs):
        """
        Convenience for setting logfile handlers for multiple apps
        simultaneously. Same as add_logfile_handler_for_app, but *prefixes can
        be supplied as a list, or a single prefix as a string, via the keyword
        arguments prefixes or prefix, respectively.
        """
        prefixes = kwargs.pop('prefixes') if 'prefixes' in kwargs \
            else [kwargs.pop('prefix', '')]
        for app in apps:
            self.add_logfile_handler_for_app(app, prefixes, **kwargs)
