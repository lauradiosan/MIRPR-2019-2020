import json
import math
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def extract_from_annotations_file(annotations_file_path, wanted_categories_id):
    print(annotations_file_path)

    ratios = []

    with open(annotations_file_path, 'r') as annotations_file:
        data = json.load(annotations_file)

        image_id_to_info = {}
        for image in data['images']:
            image_id = image['id']
            image_id_to_info[image_id] = image

        for annotation in data['annotations']:
            if annotation['category_id'] in wanted_categories_id:
                width = annotation['bbox'][2]
                height = annotation['bbox'][3]

                image_id = annotation['image_id']
                image_info = image_id_to_info[image_id]

                image_width = image_info['width']
                image_height = image_info['height']

                width /= image_width
                height /= image_height

                ratio = width/height
                ln_ratio = math.log(ratio)

                ratios.append(ln_ratio)

    ratios = np.array(ratios)
    plt.hist(ratios, bins=20)
    plt.axvline(ratios.mean(), color='k', linestyle='dashed', linewidth=1)
    plt.axvline(ratios.mean()+ratios.std(), color='red', linestyle='dashed', linewidth=1)
    plt.axvline(ratios.mean()-ratios.std(), color='red', linestyle='dashed', linewidth=1)
    plt.axvline(ratios.mean()+2*ratios.std(), color='red', linestyle='dashed', linewidth=1)
    plt.axvline(ratios.mean()-2*ratios.std(), color='red', linestyle='dashed', linewidth=1)
    print("Mean: ", np.exp(ratios.mean()))
    print("Mean + std: ", np.exp(ratios.mean() + ratios.std()))
    print("Mean - std: ", np.exp(ratios.mean() - ratios.std()))
    print("Mean + 2std: ", np.exp(ratios.mean() + 2*ratios.std()))
    print("Mean - 2std: ", np.exp(ratios.mean() - 2*ratios.std()))
    plt.show()


# path = sys.argv[1]
path = Path('C:\\Users\\Andrei Popovici\\Documents\\COCO')

wanted_categories_id = [1]


val_annotations_path = path / 'annotations' / 'instances_train2017.json'
extract_from_annotations_file(val_annotations_path, wanted_categories_id)
