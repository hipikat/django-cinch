"""
Base settings that exist solely to enable the creation of a SECRET_KEY
file, via a Django management command, before one has been created.
"""

from cinch import cinch_settings


G = globals()
S = G.setdefault


SECRET_KEY = '12345'


# Include our sibling default settings
G.update(cinch_settings('default', G))
