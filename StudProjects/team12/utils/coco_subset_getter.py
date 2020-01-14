import json
import shutil
from pathlib import Path


def compute_annotations_area_to_image_area(annotations, image_info):
    annotations_area = 0
    for annotation in annotations:
        annotation_width = annotation['bbox'][2]
        annotation_height = annotation['bbox'][3]

        annotations_area += annotation_width * annotation_height

    image_area = image_info['height'] * image_info['width']

    return annotations_area / image_area


def extract_from_annotations_file(annotations_file_path, folder, wanted_categories_id,
                                  destination_images, destination_annotation):
    print(annotations_file_path)
    print(folder)
    with open(annotations_file_path, 'r') as annotations_file:
        data = json.load(annotations_file)
        new_data = {'images': [], "annotations": [],  "categories": []}

        useful_images_to_labels = {}
        for annotation in data['annotations']:
            area = annotation['area']

            if annotation['category_id'] in wanted_categories_id and area > 32*32:
                image_id = annotation['image_id']

                if image_id not in useful_images_to_labels:
                    useful_images_to_labels[image_id] = []

                useful_images_to_labels[image_id].append(annotation)

        image_id_to_image_file_name = {}
        image_id_to_image_info = {}
        for image in data['images']:
            image_id_to_image_file_name[image['id']] = image['file_name']
            image_id_to_image_info[image['id']] = image

        for image_id, annotations in useful_images_to_labels.items():
            shutil.copy(folder / image_id_to_image_file_name[image_id],
                        destination_images / image_id_to_image_file_name[image_id])
            new_data['images'].append(image_id_to_image_info[image_id])
            new_data['annotations'] = new_data['annotations'] + annotations

        for category in data['categories']:
            if category['id'] in wanted_categories_id:
                new_data['categories'].append(category)

        with open(destination_annotation, 'w') as outfile:
            json.dump(new_data, outfile)


path = Path('D:\\COCO')
destination = Path('D:\\COCO_new')

wanted_categories_id = [1, 3]

train_annotations_path = path / 'annotations' / 'instances_train2017.json'
train_folder_path = path / 'train2017'
train_annotations_path_destionation = destination / 'annotations' / 'instances_train2017.json'
train_folder_path_destination = destination / 'train2017'
extract_from_annotations_file(train_annotations_path, train_folder_path, wanted_categories_id,
                              train_folder_path_destination, train_annotations_path_destionation)

val_annotations_path = path / 'annotations' / 'instances_val2017.json'
val_folder_path = path / 'val2017'
val_annotations_path_destionation = destination / 'annotations' / 'instances_val2017.json'
val_folder_path_destination = destination / 'val2017'
extract_from_annotations_file(val_annotations_path, val_folder_path, wanted_categories_id,
                              val_folder_path_destination, val_annotations_path_destionation)
