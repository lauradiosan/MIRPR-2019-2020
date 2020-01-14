import numpy as np
import cv2
from train.helpers import activations_to_bboxes
from misc.utils import *

# postprocess


def nms(bounding_boxes, predicted_classes, threshold=0.5):
    """
    args:
        bounding_boxes: nr_bboxes x 4 sorted by confidence
        threshold: bboxes with IoU above threshold will be removed

    returns:
        final_model_predictions: nr_bboxes x 4

    bounding_boxes MUST be sorted
    """
    bounding_boxes = bounding_boxes[:200]
    predicted_classes = predicted_classes[:200]

    indices = np.array(range(bounding_boxes.shape[0]))
    final_model_predictions = []
    while indices.shape[0] != 0:
        prediction = bounding_boxes[indices[0]]
        final_model_predictions.append(indices[0])

        to_keep = []
        for index in range(indices.shape[0]):
            IoU = get_IoU(prediction, bounding_boxes[indices[index]])

            if IoU < threshold or (predicted_classes[indices[0]] != predicted_classes[indices[index]]):
                to_keep.append(index)

        indices = indices[to_keep]

    return final_model_predictions


def after_nms(prediction_bboxes, predicted_confidences):
    """
    return final model preditctions
    """
    kept_after_nms = nms(prediction_bboxes)

    post_nms_bboxes = prediction_bboxes[kept_after_nms]
    post_nms_confidences = predicted_confidences[kept_after_nms]

    return post_nms_bboxes, post_nms_confidences
