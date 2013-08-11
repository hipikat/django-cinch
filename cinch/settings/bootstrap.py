"""
Base settings that exist solely to enable the creation of a SECRET_KEY
file, via a Django management command, before one has been created.
"""

from revkom.settings import base_settings_mixin


SECRET_KEY = '12345'

# Include our sibling default settings.
execfile(base_settings_mixin('default'))
