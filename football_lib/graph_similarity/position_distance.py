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

def normal_position_proximity(match_a, match_b, id_position_match_a, top_k = 5):
  a = match_a.get_signature()
  b = match_b.get_signature()
  dis = distance_matrix(a, b)
  dis = dis[id_position_match_a, :]
  indices = np.argsort(dis)
  indices = indices[:min(top_k, len(indices))]
  return indices, dis[indices]

def gaussian_position_proximity(match_a, match_b, id_position_match_a, top_k = 5, window_size = 25):
  if window_size % 2 == 0: window_size += 1
  a = match_a.get_signature()
  b = match_b.get_signature()
  dis = distance_matrix(a, b)
  gaussian_kernel = gaussian(window_size, SIGMA)
  id_position_match_a = max(id_position_match_a, window_size // 2)
  dis = dis[id_position_match_a - window_size // 2: id_position_match_a + 1 + window_size // 2, :]
  for i in range(window_size // 2):
    shift_up = i + 1
    shift_down = len(dis[0]) - (i + 1)
    dis[window_size // 2 - (i + 1)] = np.roll(dis[window_size // 2 - (i + 1)], shift_up)
    dis[window_size // 2 + (i + 1)] = np.roll(dis[window_size // 2 + (i + 1)], shift_down)
    dis[window_size // 2 - (i + 1), :(i + 1)] = INF
    dis[window_size // 2 + (i + 1),  len(dis[0]) - (i + 1):] = INF
  weights = np.transpose(np.tile(gaussian_kernel, (len(dis[0]), 1)))
  dis *= weights
  dis = np.sum(dis, axis=1)
  indices = np.argsort(dis)
  indices = indices[:min(top_k, len(indices))]
  return indices, dis[indices]

def fastdtw_position_proximity(match_a, match_b, distance_function = 'euclidean'):
  a = match_a.get_signature() 
  b = match_b.get_signature()
  global_distance, path_res = fastdtw(a, b, dist=distance_dic[distance_function])
  return global_distance, path_res

