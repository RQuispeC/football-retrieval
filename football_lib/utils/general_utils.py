from skimage.exposure import rescale_intensity

def rescale(image,intensity):
    output = rescale_intensity(image, in_range=(0, intensity))
    output = (output * intensity).astype("float")
    return output
