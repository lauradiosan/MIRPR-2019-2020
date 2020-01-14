import re
import os
import shutil
import cv2
from imgaug import augmenters as iaa

PATH = "aug_data"

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        image = cv2.imread(fullpath)

        idx = 1

        for i in range(20, 41, 20):
            noise = iaa.AdditiveGaussianNoise(scale=(i, i))
            image_aug = noise.augment_image(image)
            newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
            cv2.imwrite(newpath, image_aug)
            idx += 1

        waterlike = iaa.ElasticTransformation(alpha=45, sigma=9)
        image_aug = waterlike.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1

        for i in range(20, 41, 20):
            noise = iaa.AdditivePoissonNoise(lam=i)
            image_aug = noise.augment_image(image)
            newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
            cv2.imwrite(newpath, image_aug)
            idx += 1
        
        noise = iaa.Pepper(p=0.05)
        image_aug = noise.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1

        noise = iaa.Fliplr(p=1)
        image_aug = noise.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1

        noise = iaa.GaussianBlur(sigma=2.2)
        image_aug = noise.augment_image(image)
        newpath = fullpath[:-4] + str(idx) + fullpath[-4:]
        cv2.imwrite(newpath, image_aug)
        idx += 1