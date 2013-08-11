
from revkom.coll import EasyList


__all__ = ['SettingList']


class SettingList(EasyList):
    """ 
    An EasyList which by default is kept flat, and whose values are kept unique.
    """
    def __init__(self, *iterables, **kwargs):
        super(SettingList, self).__init__(*iterables)
        self.unique = kwargs.get('unique', True)
        self.flat = kwargs.get('flat', True)
