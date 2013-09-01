"""
Base production settings for a project to include via execfile().
"""

from cinch import cinch_settings


g = globals()
S = g.setdefault


# Debugging and development modes
S('DEBUG', False)

# Include our sibling debug settings
g.update(cinch_settings(g, 'base'))
