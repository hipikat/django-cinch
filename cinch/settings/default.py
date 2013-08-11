"""
These are the default settings used by manage.py and the default wsgi
application instance when no DJANGO_SETTINGS_MODULE environment variable
is set. They provide the minimum configuration needed to create a
running server or invoke a Django shell. Generally, a
DJANGO_SETTINGS_MODULE environment variable should be set. The author
suggests a postactivate hook in the project's virtual environment.
"""

from cinch import cinch_settings


G = globals()
S = G.setdefault


S('ADMINS', ())
S('PROJECT_NAME', 'cinch')

# Include our sibling debug settings
G.update(cinch_settings('debug', G))
