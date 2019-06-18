from skimage.exposure import rescale_intensity

import numpy as np

def rescale(image,intensity):
    output = rescale_intensity(image, in_range=(0, intensity))
    output = (output * intensity).astype("float")
    return output

# melhorar a complexidade dessa operacao
def get_signatures(match, id_player):
	output = []
	for p in match:
		sig = p.signature[id_player]
		output.append(sig)
	output = np.array(output)
	return output

def distance_matrix(query_features, gallery_features):
	"""
	Computes euclidean distance matrix between two list of features
	"""
	matrix = np.zeros((len(query_features), len(gallery_features)))
	q_pow = np.sum(query_features * query_features, axis = 1)
	g_pow = np.sum(gallery_features * gallery_features, axis = 1)
	prod = 2 * np.dot(query_features, np.transpose(gallery_features))
	matrix += np.transpose(np.tile(q_pow, (len(g_pow), 1)))
	matrix += np.tile(g_pow, (len(q_pow), 1))
	matrix -= prod
	return matrix	