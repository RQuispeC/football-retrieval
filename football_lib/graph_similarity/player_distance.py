from __future__ import absolute_import
from __future__ import division

import numpy as np

from fastdtw import fastdtw
from football_lib.utils.general_utils import get_signatures

from scipy.spatial import distance

distance_dic = {
	'euclidean': distance.euclidean,
	'cosine': distance.cosine,
	'manhattan': distance.cityblock
}

def player_proximity(match, player, distance_function):
	player_signature = get_signatures(match,player)
	function = distance_dic[distance_function]
	
	global_distance = np.inf
	player_res = player
	path_res = []

	for i in range(22):
		if i != player:
			i_signature = get_signatures(match,i)
			distance, path = fastdtw(player_signature, i_signature, dist=function)
			if distance < global_distance:
				global_distance = distance
				player_res = i
				path_res = path

	path_res = np.array(path_res)

	return global_distance, path_res, player_res
