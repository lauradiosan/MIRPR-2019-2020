import imageio
import imgaug as ia
import cv2
from imgaug import augmenters as iaa

image = cv2.imread("child.jpg")

idx = 1

for i in range(20, 41, 20):
    noise = iaa.AdditiveGaussianNoise(scale=(i, i))
    image_aug = noise.augment_image(image)
    cv2.imwrite('human_aug' + str(idx) + '.png', image_aug)
    idx += 1

waterlike = iaa.ElasticTransformation(alpha=45, sigma=9)
image_aug = waterlike.augment_image(image)
cv2.imwrite('human_aug3.png', image_aug)
idx += 1

for i in range(20, 41, 20):
    noise = iaa.AdditivePoissonNoise(lam=i)
    image_aug = noise.augment_image(image)
    cv2.imwrite('human_aug' + str(idx) + '.png', image_aug)
    idx += 1

noise = iaa.Pepper(p=0.05)
image_aug = noise.augment_image(image)
cv2.imwrite('human_aug6.png', image_aug)
idx += 1

noise = iaa.Fliplr(p=1)
image_aug = noise.augment_image(image)
cv2.imwrite('human_aug7.png', image_aug)
idx += 1

noise = iaa.GaussianBlur(sigma=2.2)
image_aug = noise.augment_image(image)
cv2.imwrite('human_aug8.png', image_aug)
idx += 1


