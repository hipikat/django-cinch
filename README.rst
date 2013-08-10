django-cinch
============

**Code Is Not Configuration. However...**

Django settings modules can rapidly get out of hand when many developers
are working on a project, especially if they're each using their own
local development settings files, and when feature branches abound, it's
easy to engineer collisions. Modularising beyond the level of singular
Python modules by way of ``from parent_module import *`` isn't ideal because
the imported modules have no knowledge of settings defined before their
import. The philosophy behind cinch is simple:

- A settings module can import other settings modules using ``execfile()``
- Your settings are the uppercase names in your ``globals()`` dict
- It's just a dict
- dict.setdefault is a really useful here

A settings module can embrace this philosophy after its imports, like so::

  G = globals()
  S = G.setdefault

With these short names defined, a well behaved settings module can define
settings only if they haven't already been defined by a child settings
module::

  S('MEDIA_URL', '/media/')

And it can reference settings which it knows have been defined earlier,
either by its own call to `S` or by the inheriting file::

  S('ROOT_URLCONF', G['PROJECT_NAME'] + '.urls')

