from __future__ import absolute_import

from .knn import *
from .threshold import *

__strategy_factory = {
  'knn': KNN,
  'threshold': Threshold,
}

def get_names():
  return list(__strategy_factory.keys())

def init_strategy(name, *args, **kwargs):
  if not name in list(__strategy_factory.keys()):
    raise KeyError("Unknown strategy: {}".format(name))
  return __strategy_factory[name](*args, **kwargs)