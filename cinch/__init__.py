
from runpy import run_module

from .caches import *
from .common import *
from .databases import *


def cinch_settings(globals_dict, name=None):
    if not name:
        name = 'prod' if not globals_dict.get('DEBUG') else 'debug'
    module_name = 'cinch.settings.' + name
    return run_module(module_name, globals_dict)
