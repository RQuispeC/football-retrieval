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

def rle(inarray):
        ia = np.asarray(inarray)
        n = len(ia)
        if n == 0: 
            return (None, None, None)
        else:
            y = np.array(ia[1:] != ia[:-1])
            i = np.append(np.where(y), n - 1)
            z = np.diff(np.append(-1, i))
            p = np.cumsum(np.append(0, z))[:-1]
            return(z, p, ia[i])

def path_processing(path, k_allowed):
	path1 = path[:,0]
	path2 = path[:,1]

	path1_info = rle(path1)
	
	acc = 0

	n = path1_info[0].shape[0]

	for i in range(n):
		length = path1_info[0][i]
		if length > k_allowed:
			init = path1_info[1][i]
			left = init - acc
			right = init - acc + length
			acc = acc + length

			path1 = np.delete(path1, np.arange(left,right))
			path2 = np.delete(path2, np.arange(left,right))

	path2_info = rle(path2)

	acc = 0

	n = path2_info[0].shape[0]

	for i in range(n):
		length = path2_info[0][i]
		if length > k_allowed:
			init = path2_info[1][i]
			left = init - acc
			right = init - acc + length
			acc = acc + length

			path1 = np.delete(path1, np.arange(left,right))
			path2 = np.delete(path2, np.arange(left,right))

	print('path1: ', path1)
	print('path2: ', path2)

	output = np.stack((path1,path2), axis=-1)

	return output


def player_proximity(match, player, k_allowed, distance_function = 'euclidean'):
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
	path_res = path_processing(path_res, k_allowed)

	return global_distance, path_res, player_res
