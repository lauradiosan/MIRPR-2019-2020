import numpy as np
from PIL import Image
from config import width, height, channels


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def img_to_array(img, path=True):
    """
    Convert image to numpy array of numbers
    :param img: image to be transformed
    :return: numpy array of image
    """
    global width, height

    if path:
        img = Image.open(img)
    img_arr = np.array(img) / 255.0
    img_arr = img_arr.reshape(width, height, channels)
    
    return img_arr