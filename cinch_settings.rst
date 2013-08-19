
***************************
Loading from cinch_settings
***************************
::

    # Access settings through the G alias
    G = globals()

    # Project name is the primary project Python module name
    PROJECT_NAME = 'hipikat'

    # Project directory is generally the 'repository root'
    PROJECT_DIR = Path(__file__).ancestor(4)
    ADMINS = [('Adam Wright', 'adam@hipikat.org')]

    # Update settings with Cinch defaults
    G.update(cinch_settings(G))

Settings provided by ``cinch_settings()``
=========================================

If any of the following are defined in your settings module (i.e. in the
dict passed to ``cinch_settings()``) before the call, they will be returned
unchanged. Thus, to diverge from any of the settings described below,
just define them in your base settings module before calling ``cinch_settings()``.

If you're making large changes to some default setting or the
setting in question is complicated, it's better to be explicit and
define it in your settings module. However, if your project makes
small changes to settings described below, you can manipulate the
variables via ``G`` in order to keep your linter happy:
::

    G['STATICFILES_DIRS'].append('/users/hipikat/my_static_files')

Django metadata
---------------

``TESTING``
    ``True`` if 'test' appears in sys.argv, otherwise ``False``.

``MANAGERS``
    Copied from ``ADMINS``.

``TIME_ZONE = "UTC"``
    Django defaults to "America/Chicago" for historical reasons.

``LANGUAGE_CODE = "en"``
    Django defaults to "en-us" for presumably americanocentric reasons.

``SITE_ID = 1``
    The default is ``None``, but this must be set if the sites framework
    is installed (i.e. if ``'django.contrib.sites'`` is in ``INSTALLED_APPS``).

``WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'``
    Your main project package provides a logical namespace for the wsgi
    module.

Directory structure
-------------------
The default Cinch project structure is inspired by conventions from the
Filesystem Hierarchy Standard wherever possible.

``LIB_DIR = PROJECT_DIR + '/lib'``
    Store third-party dependancies (besides the ones you can ``pip install``)
    in here, preferably as git submodules.

``ETC_DIR = PROJECT_DIR + '/etc'``
    Configuration files. Any files of the form UPPERCASE_NAME.setting
    found under this directory will be loaded as settings.

``VAR_DIR = PROJECT_DIR + '/var'``
    Variable data files. Everything under this directory should be
    considered transient, disposable and/or only used during development
    or testing.

``DB_DIR = VAR_DIR + '/db'``
    Database files including dumps and SQLite files.

``FIXTURE_DIRS = [VAR_DIR + '/fixtures']``
    Project and application fixtures.

``LOG_DIR = VAR_DIR + '/log'``
    Log files.

``STATIC_ROOT = VAR_DIR + '/static'``
    Destination directory for ``manage.py collectstatic``. Ideally, this
    should only be used during development, and production settings
    modules will reference an AWS S3 bucket or some such.

``MEDIA_ROOT = VAR_DIR + '/media'``
    User-uploaded files are saved here. Ideally, this
    should only be used during development, and production settings
    modules will reference an AWS S3 bucket or some such.

``TMP_DIR = VAR_DIR + '/tmp'``
    Temporary file directory, such as for build directories for docs
    or CSS/JS compilers, etc.

``SRC_DIR = PROJECT_DIR + '/src'``
    Source code for the project. This directory should be on the Python
    path.

``STATICFILES_DIRS = [SRC_DIR + '/static']``
    Static files specific to your project, as harvested by
    ``manage.py collectstatic``.

``TEMPLATE_DIRS = [SRC_DIR + '/templates']``
    Django template files. If ``'django.template.loaders.filesystem.Loader'``
    comes before ``'django.contrib.staticfiles.finders.AppDirectoriesFinder'``
    in your ``STATICFILES_FINDERS`` setting, this directory will be checked
    for templates before third-party apps' template/ directories.

``sys.path.insert(0, SRC_DIR + '/apps'))``
    If you've got third-party apps you can't or don't want to ``pip install``
    (perhaps because you're patching them and sending pull requests back
    to their authors), you can symlink them in src/apps/ to make them
    findable by Python. That is, from your project repository root
    directory::

        $ git submodule add git@github.com:hipikat/django-hostess.git lib/django-hostess
        Cloning into 'lib/foobar'...
        ...
        $ ln -s ../../lib/django-hostess/hostess src/apps/hostess

Security
--------
``CINCH_LOCAL_HOSTS = ['localhost', '127.0.0.1']``
``INTERNAL_IPS = CINCH_LOCAL_HOSTS + G.get('INTERNAL_IPS', [])``
``ALLOWED_HOSTS = CINCH_LOCAL_HOSTS + G.get('ALLOWED_HOSTS', [])``
    If you set your high-level domain name in your settings before using ``cinch_settings()``,
    ``CINCH_LOCAL_HOSTS`` will be added to the set.

