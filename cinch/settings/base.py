# pylint: disable=C0103
# C0103 - Invalid name for type. Please excuses the 'constants' g and s.
"""
Reusable base settings for Django projects. Intended usage is to set
globals in a settings file specific to an instance of a server, then
include this file via execfile().

These base settings will avoid overriding settings from including
files, while setting defaults based on the value of attributes.
"""

import sys
from unipath import Path
from django.core.exceptions import ImproperlyConfigured
from revkom.settings import SETTINGS_PATH
from revkom.settings.utils import LoggingSetting, SettingList


# Shortcuts for checking and setting default settings.
G = globals()
S = G.setdefault


# Test mode
G['TESTING'] = True if 'test' in sys.argv else False


# Check for settings which must be defined before this file is execfile()'d
S('REVKOM_REQUIRED_SETTINGS', set(['PROJECT_NAME', 'ADMINS']))
if not G['REVKOM_REQUIRED_SETTINGS'].issubset(G):
    raise ImproperlyConfigured(
        "Missing expected setting(s): %s" %
        list(G['REVKOM_REQUIRED_SETTINGS'].difference(G)))

###
# Django - Metadata
###
S('MANAGERS', G['ADMINS'])
S('TIME_ZONE', 'UTC')           # Default is "America/Chicago"
S('LANGUAGE_CODE', 'en')        # Default is "en-us"
S('SITE_ID', 1)                 # Default is not defined
S('WSGI_APPLICATION', G['PROJECT_NAME'] + '.wsgi.application')

###
# Directory structure
###
# Project directory is the repository root.
S('PROJECT_DIR', SETTINGS_PATH.ancestor(3))
# Only fixtures, static and template directories are used internally by Django.
S('LIB_DIR', G['PROJECT_DIR'].child('lib'))              # lib/
S('VAR_DIR', G['PROJECT_DIR'].child('var'))              # var/
S('CONF_DIR', G['VAR_DIR'])                              # var/
S('DB_DIR', G['VAR_DIR'].child('db'))                    # var/db/
S('FIXTURE_DIRS', [G['VAR_DIR'].child('fixtures'),])     # var/fixtures/
S('LOG_DIR', G['VAR_DIR'].child('log'))                  # var/log/
S('STATIC_ROOT', G['VAR_DIR'].child('static'))           # var/static/
S('MEDIA_ROOT', G['VAR_DIR'].child('media'))             # var/media/
S('TMP_DIR', G['VAR_DIR'].child('tmp'))                  # var/tmp/
S('SRC_DIR', G['PROJECT_DIR'].child('src'))              # src/
S('STATICFILES_DIRS', [G['SRC_DIR'].child('static'),])   # src/static/
S('TEMPLATE_DIRS', [G['SRC_DIR'].child('templates'),])   # src/templates/
sys.path.insert(0, G['SRC_DIR'].child('apps'))           # src/apps/

###
# Security
###
# Host/domain names that are valid for this site; required if DEBUG is False.
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
S('REVKOM_LOCAL_HOSTS', ['localhost', '127.0.0.1'])
ALLOWED_HOSTS = SettingList(G.get('ALLOWED_HOSTS'), REVKOM_LOCAL_HOSTS)
INTERNAL_IPS = SettingList(G.get('INTERNAL_IPS'), REVKOM_LOCAL_HOSTS)


# By default we look for a secret key in var/SECRET_KEY. New secret keys
# can be generated by running `scripts/make_secret_key.py'
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
S('SECRET_KEY_FILE', G['CONF_DIR'].child('SECRET_KEY'))
if 'SECRET_KEY' not in G:
    if 'SECRET_KEY_FILE' in G and Path(G['SECRET_KEY_FILE']).exists():
        SECRET_KEY = G['SECRET_KEY_FILE'].read_file()
    elif G['CONF_DIR'].child('SECRET_KEY').exists():
        SECRET_KEY = G['CONF_DIR'].child('SECRET_KEY').read_file()

###
# Debugging and development modes
###
S('DEBUG', False)

###
# Logging
###
# http://docs.djangoproject.com/en/dev/topics/logging
S('LOGGING', LoggingSetting({
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
}, logfile_dir=G['LOG_DIR']))

###
# Databases
###
if 'DATABASES' not in G:
    DATABASES = DatabasesSetting()['default'] = \
        db_setting(engine='sqlite3', name=G['DB_DIR'].child('default.db'))

###
# Caching
###
S('CACHE_MIDDLEWARE_ANONYMOUS_ONLY', True)
if 'CACHES' not in G:
    CACHES = CachesSetting()['default'] = {'backend': 'LocMemCache'}

###
# URLs
###
S('ROOT_URLCONF', G['PROJECT_NAME'] + '.urls')
S('MEDIA_URL', '/media/')
S('STATIC_URL', '/static/')

###
# Django - Feature switches
###
S('USE_I18N', True)     # Internationalisation framework
S('USE_L10N', True)     # Localisation framework
S('USE_TZ', True)       # Timezone support for dates

###
# Django - File discovery
###
# List of finder classes that know how to find static files.
S('STATICFILES_FINDERS', SettingList(
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
))

# List of callables that know how to import templates.
S('TEMPLATE_LOADERS', SettingList(
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
))
# Used by Revkom's CustomFileFinder, for cherry-picking static files
# A dictionary of the form { static_path: filesystem_path, ... }
S('REVKOM_STATICFILES', {})

###
# Django - request pipline
###
# https://docs.djangoproject.com/en/dev/topics/http/middleware/
S('MIDDLEWARE_CLASSES', SettingList(
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
))

###
# Django - Installed apps
###
S('INSTALLED_APPS', SettingList(
    'revkom',
    # django-extensions: shell_plus, runserver_plus, etc.
    # http://packages.python.org/django-extensions/
    'django_extensions',
    # South: Database-agnostic migrations for Django applications.
    # http://south.readthedocs.org
    'south',
    # Django contrib packages
    # https://docs.djangoproject.com/en/dev/ref/contrib/
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
))
