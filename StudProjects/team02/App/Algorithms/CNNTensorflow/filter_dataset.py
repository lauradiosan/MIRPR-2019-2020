import os
from config import *
from PIL import Image


def remove_non_regular_image(image_path):
    global width, height

    img = Image.open(image_path)
    w, h = img.size
    if w != width or h != height:
        return True
    return False


def filter_dataset(dataset_location):
    samples_free = dataset_location + label_free
    samples_occupied = dataset_location + label_occupied

    images_free = os.listdir(samples_free)
    images_occupied = os.listdir(samples_occupied)

    filtered = []
    for img in images_free:
        img_path = samples_free + img
        if remove_non_regular_image(img_path):
            filtered.append("dataset\\free\\" + img)

    for img in images_occupied:
        img_path = samples_occupied + img
        if remove_non_regular_image(img_path):
            filtered.append("dataset\\busy\\" + img)

    for img in filtered:
        print(img)
        os.remove(img)


if __name__ == '__main__':
    filter_dataset(train_dataset)