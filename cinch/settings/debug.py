"""
Base debug settings for a project to include via execfile().
"""

from cinch import cinch_settings


g = globals()
S = g.setdefault


# Debugging and development modes
S('DEBUG', True)
S('TEMPLATE_DEBUG', g['DEBUG'])
S('TEMPLATE_STRING_IF_INVALID', 'INVALID_CONTEXT[%s]')

# Include our sibling base settings
g.update(cinch_settings(g, 'base'))

# Directory structure
S('MEDIA_ROOT', g['TMP_DIR'].child('media'))

# Django - request pipeline
g['MIDDLEWARE_CLASSES'].append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Django - installed apps
g['INSTALLED_APPS'].append(
    # django-debug-toolbar: A configurable set of panels that display
    # various debug information about the current request/response.
    # https://github.com/django-debug-toolbar/django-debug-toolbar
    'debug_toolbar'
)
