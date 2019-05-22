from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat

import numpy as np

__all__ =  ['Degree']

class Degree(object):
	def __init__(self, *args, **kwargs):
		pass

	def __call__(self, position):
		deg_team_a = np.zeros(position.edges_team_a.shape[0])
		deg_team_b = np.zeros(position.edges_team_b.shape[0])

		temp = int(position.edges_team_b[0,0])

		edges_team_a_u = np.array(position.edges_team_a[:,0]).astype(int)
		unique_a_u, counts_a_u = np.unique(edges_team_a_u, return_counts=True)

		edges_team_a_v = np.array(position.edges_team_a[:,1]).astype(int)
		unique_a_v, counts_a_v = np.unique(edges_team_a_v, return_counts=True)

		edges_team_b_u = np.array(position.edges_team_b[:,0]).astype(int)
		edges_team_b_u = edges_team_b_u - temp
		unique_b_u, counts_b_u = np.unique(edges_team_b_u, return_counts=True)

		edges_team_b_v = np.array(position.edges_team_b[:,1]).astype(int)
		edges_team_b_v = edges_team_b_v - temp
		unique_b_v, counts_b_v = np.unique(edges_team_b_v, return_counts=True)

		deg_team_a[unique_a_u] = deg_team_a[unique_a_u] + counts_a_u
		deg_team_a[unique_a_v] = deg_team_a[unique_a_v] + counts_a_v
		
		deg_team_b[unique_b_u] = deg_team_b[unique_b_u] + counts_b_u
		deg_team_b[unique_b_v] = deg_team_b[unique_b_v] + counts_b_v

		rep = np.array([deg_team_a, deg_team_b])
		rep = rep.reshape(-1)

		return rep