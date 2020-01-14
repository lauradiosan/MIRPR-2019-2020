import re
import os
import shutil
import cv2
from imgaug import augmenters as iaa

PATH = "aug_data2"

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        image = cv2.imread(fullpath)

        idx = 10

        noise = iaa.AdditiveGaussianNoise(scale=(30, 30))
        image_aug = noise.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1

        noise = iaa.AdditivePoissonNoise(lam=30)
        image_aug = noise.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1
        
        noise = iaa.Pepper(p=0.05)
        image_aug = noise.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1
