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