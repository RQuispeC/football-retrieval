from __future__ import absolute_import

import numpy as np

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

	output = np.stack((path1,path2), axis=-1)

	return output