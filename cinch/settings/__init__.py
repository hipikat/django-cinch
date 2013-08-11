"""
This package facilitates the provision of organised, pre-configured
Django projects, by providing boilerplate settings for a typical medium-
sized web site. I.e. a site with a modicum of bespoke code, but shy of
what you'd call "web scale"- your typical skunkworks job.

TODO: Highlight features!
"""

from inspect import currentframe, getfile
from unipath import Path


__all__ = ['SETTINGS_PATH', 'base_settings_mixin']


SETTINGS_PATH = Path(getfile(currentframe())).parent


def base_settings_mixin(settings='base', abstract=True):
    """
    Returns the absolute path to a (presumed existing) settings mixin.
    Intended to be passed to execfile(), when some concrete settings file
    wishes to extend a base file.
    """
    return SETTINGS_PATH.child('%s%s.py' % ('_' if abstract else '', settings))


#class PythonNameList(list):
#    """
#    A list of strings representing Python dotted names, or actual objects.
#    """
#    def __init__(self, iterable=None,
#                 allow_objects=True, allow_strings=True, *args):
#        """
#        """
#        super(PythonNameList, self).__init__(iterable)
#        for arg in args:
#            self.
