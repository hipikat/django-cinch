
from runpy import run_module

from .caches import *
from .common import *
from .databases import *


def cinch_settings(globals_dict, **kwargs):
    module_name = 'cinch.settings.'
    module_name += kwargs.get('name', 'prod' if not globals_dict.get('DEBUG') else 'debug')
    return run_module(module_name, globals_dict)
