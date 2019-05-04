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