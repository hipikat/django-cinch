"""
Base settings that exist solely to enable the creation of a SECRET_KEY
file, via a Django management command, before one has been created.
"""

from cinch import cinch_settings


g = globals()
S = g.setdefault


SECRET_KEY = '12345'


# Include our sibling default settings
g.update(cinch_settings(g, 'default'))
