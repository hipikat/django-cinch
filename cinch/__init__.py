
from runpy import run_module
from .caches import *
from .common import *
from .databases import *


def cinch_settings(globals_dict, **kwargs):
    settings_module = 'cinch.settings.'
    settings_module += kwargs.get('name', 'prod' if not globals_dict.get('DEBUG') else 'debug')
    return run_module(settings_module, globals_dict)
