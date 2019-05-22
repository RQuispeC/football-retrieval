from __future__ import absolute_import

from .space import *
from .degree import *

__representation_factory = {
  'space': Space,
  'degree': Degree
}

def get_names():
  return list(__representation_factory.keys())

def init_representation(name, *args, **kwargs):
  if not name in list(__representation_factory.keys()):
    raise KeyError("Unknown representation: {}".format(name))
  return __representation_factory[name](*args, **kwargs)