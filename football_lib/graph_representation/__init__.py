from __future__ import absolute_import

from .space import *
from .degree import *
from .eccentricity import *
from .gEfficiency import *

__representation_factory = {
  'space': Space,
  'degree': Degree,
  'eccentricity': Eccentricity,
  'gEfficiency': Gefficiency
}

def get_names():
  return list(__representation_factory.keys())

def init_representation(name, *args, **kwargs):
  if not name in list(__representation_factory.keys()):
  	raise KeyError("Unknown representation: {}".format(name))
  return __representation_factory[name](*args, **kwargs)