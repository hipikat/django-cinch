"""
Base production settings for a project to include via execfile().
"""

from cinch import cinch_settings


G = globals()
S = G.setdefault


# Debugging and development modes
S('DEBUG', False)

# Include our sibling debug settings
G.update(cinch_settings('base', G))
