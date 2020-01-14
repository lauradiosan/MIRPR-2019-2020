import matplotlib.pyplot as plot
import numpy as np
import cv2
import random
import skimage.measure

img1 = cv2.imread("child.jpg")
img1 = cv2.resize(img1, (480, 480))
img = np.array(img1, np.float32)

kernel = np.array([[[1, 1, 1], [0, 0, 0], [-1, -1, -1]], [[2, 2, 2], [0, 0, 0], [-2, -2, -2]], [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]])
# kernel2 = np.array([[[1, 1, 1], [0, 0, 0], [-1, -1, -1]], [[2, 2, 2], [0, 0, 0], [-2, -2, -2]], [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]])

def u(i, j):
    return sum(sum(img[i-1:i+2, j-1:j+2, :] * kernel))


new_img = np.zeros(img.shape, np.float32)


for i in range(1, img.shape[0] - 1):
    for j in range(1, img.shape[1] - 1):
        new_img[i, j] = u(i, j)

cv2.normalize(new_img, new_img, 0, 255, cv2.NORM_MINMAX, dtype=-1)
new_img = new_img.astype(np.uint8)


norm_img = img + new_img
cv2.normalize(norm_img, norm_img, 0, 255, cv2.NORM_MINMAX, dtype=-1)
norm_img = norm_img.astype(np.uint8)

cv2.imshow("img", img1)
cv2.imshow("img2", new_img)

a = cv2.cvtColor(new_img, cv2.COLOR_RGB2GRAY)

cv2.imshow("img3", skimage.measure.block_reduce(a, (3, 3), np.max))

cv2.waitKey(0)