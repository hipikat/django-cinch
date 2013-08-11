"""
Base production settings for a project to include via execfile().
"""

from revkom.settings import base_settings_mixin


G = globals()
S = G.setdefault


# Debugging and development modes
S('DEBUG', False)

# Include our sibling base settings. (Note: this also sets s and g.)
execfile(base_settings_mixin('base'))
