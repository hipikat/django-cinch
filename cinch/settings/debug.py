"""
Base debug settings for a project to include via execfile().
"""

from cinch import cinch_settings


G = globals()
S = G.setdefault


# Debugging and development modes
S('DEBUG', True)
S('TEMPLATE_DEBUG', G['DEBUG'])
S('TEMPLATE_STRING_IF_INVALID', 'INVALID_CONTEXT[%s]')

# Include our sibling base settings
G.update(cinch_settings('base', G))

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
