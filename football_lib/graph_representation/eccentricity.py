from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat

import numpy as np

__all__ =  ['Eccentricity']

class Eccentricity(object):
	def __init__(self, *args, **kwargs):
		pass

	def __call__(self, position):
		rep = np.array([1,2,3])
		rep = rep.reshape(-1)

		return rep