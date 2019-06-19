from __future__ import absolute_import
from __future__ import division

import os
import sys
sys.path.append(os.getcwd())

from football_lib.utils.edgestools import dist_mat
from football_lib.utils.edgestools import convert_to_matrix

from football_lib.utils import graphPath_algorithms

import numpy as np

__all__ =  ['Gefficiency']
np.seterr(divide='ignore')

class Gefficiency(object):
    def __init__(self, match, *args, **kwargs):
        self.V = 11

    def __call__(self, position):
        edges_ta = position.edges_team_a.copy() #[]
        edges_tb = position.edges_team_b.copy() #[]
        matrix_team_a = convert_to_matrix(edges_ta, self.V)
        matrix_team_b = convert_to_matrix(edges_tb, self.V)

        dist_team_a = graphPath_algorithms.floyd_warshall(matrix_team_a)
        dist_team_b = graphPath_algorithms.floyd_warshall(matrix_team_b)

        gefficiency_team_a = self._global_efficiency(dist_team_a)
        gefficiency_team_b = self._global_efficiency(dist_team_b)

        rep = np.array([gefficiency_team_a, gefficiency_team_b])
        rep = rep.reshape(-1)

        return rep

    def _global_efficiency(self, dist):
        sp = np.asarray(dist) # = dist.shape[0]
        temp = 1.0 / sp
        
        np.fill_diagonal(temp, 0)
        N = temp.shape[0]
        
        ne = (1.0 / (N - 1)) * np.apply_along_axis(sum, 0, temp)

        return ne