import json
from pathlib import Path


def extract_from_annotations_file(annotations_file_path, folder, destination_annotation):
    print(annotations_file_path)
    print(folder)
    with open(annotations_file_path, 'r') as annotations_file:
        data = json.load(annotations_file)
        new_data = {'images': [], "annotations": [],  "categories": data['categories']}

        wanted_image_ids = set()
        for i in range(256):
            wanted_image_ids.add(data['images'][i]['id'])
            new_data['images'].append(data['images'][i])

        for annotation in data['annotations']:
            if annotation['image_id'] in wanted_image_ids:
                new_data['annotations'].append(annotation)

        with open(destination_annotation, 'w') as outfile:
            json.dump(new_data, outfile)


path = Path('C:\\Users\\Andrei Popovici\\Documents\\COCO')
destination = Path('C:\\Users\\Andrei Popovici\\Documents\\COCO')

wanted_categories_id = [1, 3]

val_annotations_path = path / 'annotations' / 'instances_val2017.json'
val_folder_path = path / 'val2017'
val_annotations_path_destionation = destination / 'annotations' / 'instances_val2017_small.json'
val_folder_path_destination = destination / 'val2017'
extract_from_annotations_file(val_annotations_path, val_folder_path,
                              val_annotations_path_destionation)
