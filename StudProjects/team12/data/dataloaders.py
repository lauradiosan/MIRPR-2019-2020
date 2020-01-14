import torchvision
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from data.dataset import CocoDetection
from torch.utils.data.sampler import *
import json


def get_dataloaders(params):
    ''' creates and returns train and validation data loaders '''

    train_annotations_path = '..\\..\\COCO\\annotations\\instances_train2017.json'
    train_dataset = CocoDetection(root='..\\..\\COCO\\train2017',
                                       annFile=train_annotations_path,
                                       augmentation=True)

    val_annotations_path = '..\\..\\COCO\\annotations\\instances_val2017.json'
    validation_dataset = CocoDetection(root='..\\..\\COCO\\val2017',
                                       annFile=val_annotations_path,
                                       augmentation=False)

    with open(train_annotations_path) as json_file:
        data = json.load(json_file)
        nr_images_in_train = len(data['images'])

    train_dataloader = DataLoader(train_dataset, batch_size=None,
                                  shuffle=False, num_workers=4,
                                  sampler=BatchSampler(SubsetRandomSampler([i for i in range(nr_images_in_train)]),
                                                       batch_size=params.batch_size, drop_last=True))

    with open(val_annotations_path) as json_file:
        data = json.load(json_file)
        nr_images_in_val = len(data['images'])

    valid_dataloader = DataLoader(validation_dataset, batch_size=None,
                                  shuffle=False, num_workers=4,
                                  sampler=BatchSampler(SequentialSampler([i for i in range(nr_images_in_val)]),
                                                       batch_size=params.batch_size, drop_last=True))

    return train_dataloader, valid_dataloader
