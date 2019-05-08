from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat

import numpy as np

__all__ =  ['Threshold']

class Threshold(object):
  def __init__(self, thr = 40, *args, **kwargs):
    self.thr = thr

  def __call__(self, match):
    edges_team_a = self._thr(match.team_a)
    edges_team_b = self._thr(match.team_b)
    return edges_team_a, edges_team_b

  def _thr(self, team):
    dmat = dist_mat(team)
    valid = (dmat <= self.thr)
    edges = []
    tsize = team.size()
    players_id = team.ID()
    for i in range(tsize):
      for j in range(i + 1, tsize):
        if valid[i, j]:
          edges.append([players_id[i], players_id[j], dmat[i, j]])
    edges = np.array(edges)
    return edges