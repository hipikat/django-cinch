
from .mixins import FHSDirsMixin

class FHSDirs(FHSDirsMixin):
    """
    A concrete subclass of `FHSDirsMixin`, this class will return an
    instantiated object with FHSDir-style attribute on it if you pass it
    a base directory, or a class that will return the same from
    `klass.setup(project_path[, force=False])`, or just by setting the
    `klass.PROJECT_PATH` attribute.
    """
    def __new__(cls, project_path=None, *args, **kwargs):
        if project_path:
            inst = cls()
            inst.PROJECT_PATH = project_path
            inst.setup()
            return inst
        else:
            return super(FHSDirs, cls).__new__(cls, *args, **kwargs)
