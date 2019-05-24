from __future__ import absolute_import

import numpy as np
import math

def distance(player_a, player_b):
  return math.sqrt((player_a.x - player_b.x)**2 + (player_a.y - player_b.y)**2)

def dist_mat(team):
  tsize = team.size()
  distance_matrix = np.zeros((tsize, tsize))
  for i in range(tsize):
    for j in range(i, tsize):
      d = distance(team.players[i], team.players[j])
      distance_matrix[i, j] = d
      distance_matrix[j, i] = d
  return distance_matrix

def convert_to_matrix(team, n):
	temp = int(team[0,0])
	team[:,0] = team[:,0] - temp
	team[:,1] = team[:,1] - temp

	_matrix = np.full((n,n), np.inf)

	edges_team_u = np.array(team[:,0]).astype(int)
	edges_team_v = np.array(team[:,1]).astype(int)
	edges_team_w = np.array(team[:,2])

	for i in range(team.shape[0]):
		_matrix[edges_team_u[i],edges_team_v[i]] = edges_team_w[i]
		_matrix[edges_team_v[i],edges_team_u[i]] = edges_team_w[i]

	for i in range(n):
		_matrix[i,i] = 0.0

	return _matrix