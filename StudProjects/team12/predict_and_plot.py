from misc.postprocessing import nms, plot_bounding_boxes
from train.helpers import *
from train.config import Params
from general_config import anchor_config
from data import dataloaders
from architectures.models import SSDNet
from visualize import anchor_mapping
from misc.model_output_handler import *

import cv2
import numpy as np

import torch
import torch.nn as nn


def model_output_pipeline(params_path, model_outputs=False, visualize_anchors=False, visualize_anchor_gt_pair=False):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    params = Params(params_path)

    if params.model_id == 'ssdnet':
        model = SSDNet.SSD_Head(params.n_classes, anchor_config.k_list)
    model.to(device)

    if model_outputs:
        checkpoint = torch.load('misc/experiments/{}/model_checkpoint'.format(params.model_id))
        model.load_state_dict(checkpoint['model_state_dict'])
        print('Model loaded successfully')
        model.eval()

    _, valid_loader = dataloaders.get_dataloaders(params)

    with torch.no_grad():
        total_iou, total_maps = 0, np.array([0, 0, 0, 0, 0, 0])
        for batch_idx, (batch_images, batch_targets, images_info) in enumerate(valid_loader):
            if model_outputs:
                batch_images = batch_images.to(device)
                predictions = model(batch_images)
            else:
                predictions = [torch.randn(params.batch_size, anchor_config.total_anchors, 4),
                               torch.randn(params.batch_size, anchor_config.total_anchors, params.n_classes)]

            for idx in range(len(batch_images)):
                iou, maps = anchor_mapping.test_anchor_mapping(
                    image=batch_images[idx], bbox_predictions=predictions[0][idx], classification_predictions=predictions[1][idx],
                    gt_bbox=batch_targets[0][idx], gt_class=batch_targets[1][idx], image_info=images_info[idx], params=params,
                    model_outputs=model_outputs, visualize_anchors=visualize_anchors, visualize_anchor_gt_pair=visualize_anchor_gt_pair)
                total_iou += iou
                total_maps += maps

            avg = (batch_idx + 1) * params.batch_size
            print("Mean iou so far: ", total_iou / avg)
            print("Mean maps so far: ", total_maps / avg)
            if batch_idx == 10:
                return
