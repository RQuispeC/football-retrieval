from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat

import numpy as np

__all__ =  ['Space']

class Space(object):
  def __init__(self, *args, **kwargs):
    pass

  def __call__(self, position):
    print('arestas: ',position.edges_team_a[:,1])
    rep = np.array([position.team_a.X(), position.team_a.Y(), position.team_b.X(), position.team_b.Y()])
    rep = rep.reshape(-1)
    return rep