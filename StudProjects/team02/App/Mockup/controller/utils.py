import numpy as np
from PIL import Image
import cv2
from controller.config import width, height, channels


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


def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final
