django-cinch
============

**Code Is Not Configuration. However...**

Django settings modules can rapidly get out of hand when many developers
are working on a project, especially if they're each using their own
local development settings. And when feature branches abound, it's
easy to engineer collisions.

Settings are a dict and that is all
-----------------------------------

Modularising beyond the level of singular
Python modules by way of ``from parent_module import *`` isn't ideal because
the imported modules have no knowledge of settings defined before their
import. The philosophy behind cinch is simple:

- A settings module can import other modules using ``execfile()``
- Your settings are the uppercase names in your ``globals()`` dict
- It's just a dict
- ``dict.setdefault()`` is a really useful here.

A settings module can embrace this philosophy like so::

  G = globals()
  S = G.setdefault

With these short names defined, a well behaved settings module can define
settings only if they haven't already been defined by a child settings
module::

  S('MEDIA_URL', '/media/')
  S('CACHE_MIDDLEWARE_KEY_PREFIX', 'my-dev')

And it can reference settings which it knows have been defined earlier,
possibly by its own call to ``S``. Accessing settings via ``G`` is a way of
declaring that you know they're set to *something* at this point, without
freaking out your linter_::

  S('ROOT_URLCONF', G['PROJECT_NAME'] + '.urls')
  G['ALLOWED_HOSTS'].append('.my-local-domain.com')
  if G.get('TESTING', False):
      G['DATABASES']['default'] = db_setting(engine='sqlite3',
                                             name=G['DB_DIR'].child('dev-test.db'))

.. _linter: http://www.pylint.org

Utility classes for Django's settings
-------------------------------------
