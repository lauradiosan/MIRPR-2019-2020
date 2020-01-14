# import the necessary packages
import sys
import numpy as np
import cv2
sys.path.append('../')
from misc.postprocessing import *
from train.helpers import *
# construct a list containing the images that will be examined
# along with their respective bounding boxes


def test():
    images = [
        ("0.png", np.array([
            (12, 84, 140, 212),
            (24, 84, 152, 212),
            (36, 84, 164, 212),
            (12, 96, 140, 224),
            (24, 96, 152, 224),
            (24, 108, 152, 236)])),
        ("1.png", np.array([
            (114, 60, 178, 124),
            (120, 60, 184, 124),
            (114, 66, 178, 130)])),
        ("2.png", np.array([
            (12, 30, 76, 94),
            (12, 36, 76, 100),
            (72, 36, 200, 164),
            (84, 48, 212, 176)]))]

    print("BUCCII")
    # loop over the images
    for (imagePath, boundingBoxes) in images:
        # load the image and clone it
        print("Initial number of bounding boxes " + str(len(boundingBoxes)))
        image = cv2.imread(imagePath)

        print(type(image))
        orig = image.copy()

        # loop over the bounding boxes for each image and draw them
        plot_bounding_boxes(orig, boundingBoxes)

        # perform non-maximum suppression on the bounding boxes
        kept_after_nms = nms(boundingBoxes, 0.3)
        print("After applying non-maximum suppression " +
              str(len(boundingBoxes[kept_after_nms])))

        # loop over the picked bounding boxes and draw them
        plot_bounding_boxes(image, boundingBoxes[kept_after_nms], 1)
