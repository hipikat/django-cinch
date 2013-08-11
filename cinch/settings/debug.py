"""
Base debug settings for a project to include via execfile().
"""

from revkom.settings import base_settings_mixin


G = globals()
S = G.setdefault


# Debugging and development modes
S('DEBUG', True)
S('TEMPLATE_STRING_IF_INVALID', 'INVALID_CONTEXT[%s]')
S('TEMPLATE_DEBUG', G['DEBUG'])

# Include our sibling base settings.
execfile(base_settings_mixin('base'))

# Directory structure
S('MEDIA_ROOT', G['TMP_DIR'].child('media'))

# Django - request pipeline
G['MIDDLEWARE_CLASSES'].append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Django - installed apps
G['INSTALLED_APPS'].append(
    # django-debug-toolbar: A configurable set of panels that display
    # various debug information about the current request/response.
    # https://github.com/django-debug-toolbar/django-debug-toolbar
    'debug_toolbar'
)
