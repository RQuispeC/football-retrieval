from __future__ import absolute_import
from __future__ import division

import numpy as np
from scipy.signal import gaussian
from fastdtw import fastdtw
from scipy.spatial import distance

from football_lib.utils.general_utils import distance_matrix

SIGMA = 15
INF = 1e15

distance_dic = {
  'euclidean': distance.euclidean,
  'cosine': distance.cosine,
  'manhattan': distance.cityblock
}

def fastdtw_team_proximity(team_features, search_matches, distance_function = 'euclidean'):
  global_distance = np.inf
  path_res = []
  best_team = -1
  for i, m in enumerate(search_matches):
    features = m.get_signature()
    team_a = features[:, 0, :]
    team_b = features[:, 1, :]
    distance, path = fastdtw(team_features, team_a, dist=distance_dic[distance_function])
    if distance < global_distance:
      global_distance = distance
      best_team = (i, 0)
      path_res = path
    distance, path = fastdtw(team_features, team_b, dist=distance_dic[distance_function])
    if distance < global_distance:
      global_distance = distance
      best_team = (i, 1)
      path_res = path
  return global_distance, path_res, best_team


