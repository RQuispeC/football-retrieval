from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat

import numpy as np

__all__ =  ['KNN']

class KNN(object):
  def __init__(self, k = 1, *args, **kwargs):
    self.k = k

  def __call__(self, position):
    edges_team_a = self._knn(position.team_a)
    edges_team_b = self._knn(position.team_b)
    return edges_team_a, edges_team_b

  def _knn(self, team):
    dmat = dist_mat(team)
    indices = np.argsort(dmat, axis=1)
    indices = indices[:,1: self.k + 1]
    players_id = team.ID()
    edges = []
    tsize = team.size()
    for i in range(tsize):
      for j in indices[i]:
        edges.append([players_id[i], players_id[j], dmat[i, j]])
    edges = np.array(edges)
    return edges