
from .mixins import FHSDirsMixin

class FHSDirs(FHSDirsMixin):
    """
    A concrete subclass of `FHSDirsMixin`, this class will return an
    instantiated object with FHSDir-style attribute on it if you pass it
    a base directory, or a class that will return the same from
    `klass.setup(base_dir[, force=False])`, or just by setting the
    `klass.BASE_DIR` attribute.
    """
    def __new__(cls, base_dir=None, *args, **kwargs):
        if base_dir:
            inst = cls()
            inst.BASE_DIR = base_dir
            inst.setup()
            return inst
        else:
            return super(FHSDirs, cls).__new__(cls, *args, **kwargs)
