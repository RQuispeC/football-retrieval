from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat
from football_lib.utils.edgestools import convert_to_matrix

import numpy as np

__all__ =  ['Eccentricity']

INF = 1e15

class Eccentricity(object):
	def __init__(self, match, *args, **kwargs):
		pass

	def __call__(self, position):
		edges_t_a = position.edges_team_a.copy()
		edges_t_b = position.edges_team_b.copy()

		matrix_team_a = convert_to_matrix(edges_t_a, 11)
		matrix_team_b = convert_to_matrix(edges_t_b, 11)

		dist_team_a = self._floyd_warshall(matrix_team_a)
		dist_team_b = self._floyd_warshall(matrix_team_b)

		for i in range(dist_team_a.shape[1]):
			if dist_team_a[0,i] >= INF:
				dist_team_a[:,i] -= INF

		for i in range(dist_team_b.shape[1]):
			if dist_team_b[0,i] >= INF:
				dist_team_b[:,i] -= INF

		eccent_team_a = self._eccent(dist_team_a)
		eccent_team_b = self._eccent(dist_team_b)

		rep = np.array([eccent_team_a, eccent_team_b])
		rep = rep.reshape(-1)

		return rep

	def _floyd_warshall(self, graph):
		dist = graph.copy()

		v = graph.shape[0]

		for k in range(v):
			for i in range(v):
				for j in range(v):
					if dist[i,k] + dist[k,j] < dist[i,j]: 
						dist[i,j] = dist[i,k] + dist[k,j]

		return dist

	def _eccent(self, dist):
		n = dist.shape[0]
		res = np.zeros(dist.shape[0])

		for i in range(n):
			res[i] = np.max(dist[i,:])

		return res