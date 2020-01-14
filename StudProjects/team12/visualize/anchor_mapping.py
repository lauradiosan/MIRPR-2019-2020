import torch
from torch import nn
import numpy as np
import random

from train.helpers import *
from misc import postprocessing
from misc.utils import *
from misc.model_output_handler import *
from general_config import anchor_config


def visualize_anchor_sets(image, anchor_grid, grid_size, k, size, zoom, ratio):
    """
    prints all anchors of a (scale, ratio) in the grid
    """
    zooms_and_ratios = [(z, r) for z in zoom for r in ratio]
    for i in range(k):
        cur_anchors = []
        for j in range(grid_size**2):
            if random.random() > 1 - (1 / grid_size):
                cur_anchors.append(anchor_grid[i + j*k])
        cur_zoom, cur_ratio = zooms_and_ratios[i]
        cur_anchors = np.array(cur_anchors)
        plot_bounding_boxes(image=image, bounding_boxes=cur_anchors,
                            classes=np.ones(cur_anchors.shape), bbox_type="anchor",
                            message="Grid size: " + str(grid_size) + " Zoom: " + str(cur_zoom) + " Ratio: " + str(cur_ratio), size=size)


def visualize_all_anchor_types(image, anchors, size, sizes_ks_zooms_ratios):
    """
    visually inspect all anchors
    """
    slice_idx = 0
    for (grid_size, k, zoom, ratio) in sizes_ks_zooms_ratios:
        if k == 0:
            continue
        visualize_anchor_sets(image=image, anchor_grid=anchors[slice_idx:slice_idx+grid_size**2 * k],
                              grid_size=grid_size, k=k, size=size, zoom=zoom, ratio=ratio)
        slice_idx += grid_size**2 * k

def mapping_per_set(pos_idx, sizes_ks_zooms_ratios):
    """
    returns the number of mapped anchors from each grid
    """
    grid_maps = [0, 0, 0, 0, 0, 0]
    grid_threshold = [size**2 * k for (size, k, _, _) in sizes_ks_zooms_ratios]
    for i in range(1, len(grid_threshold)):
        grid_threshold[i] += grid_threshold[i-1]

    for idx in pos_idx:
        if idx < grid_threshold[0]:
            grid_maps[0] += 1
        elif idx < grid_threshold[1] :
            grid_maps[1] += 1
        elif idx < grid_threshold[2]:
            grid_maps[2] += 1
        elif idx < grid_threshold[3]:
            grid_maps[3] += 1
        elif idx < grid_threshold[4]:
            grid_maps[4] += 1
        else:
            grid_maps[5] += 1

    print("Anchors per grid matched this image: ", grid_maps)
    print('--------------------------------------------------------------------------------')
    print('--------------------------------------------------------------------------------')
    return np.array(grid_maps)

def mean_mapping_IOU(image, anchors, pos_idx, gt_bbox_for_matched_anchors, gt_classes_for_matched_anchors, size, sizes_ks_zooms_ratios, visualize_anchor_gt_pair):
    """
    Checks how well anchors match ground truth bboxes
    returns the mean IoU of mapped anchors, plots pairs of anchor/gt bboxes
    """
    ious = []
    for i in range(pos_idx.shape[0]):
        cur_iou = get_IoU(anchors[pos_idx[i]], gt_bbox_for_matched_anchors[i])
        ious.append(cur_iou)
        if visualize_anchor_gt_pair:
            cur_grid = list(mapping_per_set([pos_idx[i]], sizes_ks_zooms_ratios=sizes_ks_zooms_ratios)).index(1)
            plot_anchor_gt(image, anchors[pos_idx[i]],
                           gt_bbox_for_matched_anchors[i], gt_classes_for_matched_anchors[i],
                           message="Anchor/GT pair IoU: " + str(cur_iou) + " Grid " + str(cur_grid), size=size)

    ious = np.array(ious)
    print("Mean anchor mapping IoU for this image: ", ious.mean())
    print("Sorted: ", sorted(ious))
    print('--------------------------------------------------------------------------------------')
    return ious.mean()

def inspect_anchors(image, anchors, gt_bbox_for_matched_anchors, gt_classes_for_matched_anchors, pos_idx, size, visualize_anchors, visualize_anchor_gt_pair):
    """
    thoroughly inspect anchors and mapping
    returns the mean IoU of mapped anchors and the number of mapped anchors for each grid
    """
    sizes_ks_zooms_ratios = [(grid_size, len(v_zoom)*len(v_ratio), v_zoom, v_ratio)
                   for (grid_size,v_zoom), (_,v_ratio) in zip(anchor_config.zoom.items(), anchor_config.ratio.items())]
    if visualize_anchors:
        visualize_all_anchor_types(image=image, anchors=anchors, size=size, sizes_ks_zooms_ratios=sizes_ks_zooms_ratios)

    iou = mean_mapping_IOU(image, anchors, pos_idx, gt_bbox_for_matched_anchors, gt_classes_for_matched_anchors, size,
    sizes_ks_zooms_ratios=sizes_ks_zooms_ratios, visualize_anchor_gt_pair=visualize_anchor_gt_pair)

    maps = mapping_per_set(pos_idx, sizes_ks_zooms_ratios=sizes_ks_zooms_ratios)
    return iou, maps

def test_anchor_mapping(image, bbox_predictions, classification_predictions, gt_bbox, gt_class, image_info, params, model_outputs, visualize_anchors, visualize_anchor_gt_pair):
    """
    Args: all input is required per image

    computes:
        - image upscaled and unnormalized as numpy array
        - predicted bboxes higher than a threshold, sorted by predicted confidence, at right scale
        - gt bboxes for the image, at right scale
    """
    output_handler = Model_output_handler(
        conf_threshold=params.conf_threshold, suppress_threshold=params.suppress_threshold)

    corner_anchors = output_handler.corner_anchors
    overlaps = jaccard(gt_bbox, corner_anchors)

    prediction_bboxes, predicted_classes, highest_confidence_for_predictions, high_confidence_indeces = output_handler._get_sorted_predictions(
        bbox_predictions, classification_predictions, image_info)

    # map each anchor to the highest IOU obj, gt_idx - ids of mapped objects
    gt_bbox_for_matched_anchors, matched_gt_class_ids, pos_idx = map_to_ground_truth(
        overlaps, gt_bbox, gt_class, params)

    indeces_kept_by_nms = postprocessing.nms(prediction_bboxes, predicted_classes,
                                             output_handler.suppress_threshold)

    # get things in the right format
    image = output_handler._unnorm_scale_image(image)
    pos_idx = (pos_idx.cpu().numpy())
    gt_bbox = output_handler._rescale_bboxes(gt_bbox, image_info[1])
    gt_class = gt_class.cpu().numpy()
    bbox_predictions = output_handler._convert_bboxes_to_workable_data(
        bbox_predictions, image_info[1])
    classification_predictions = output_handler._convert_confidences_to_workable_data(
        classification_predictions)
    raw_class_ids, _ = output_handler._get_predicted_class(classification_predictions)
    gt_bbox_for_matched_anchors = output_handler._rescale_bboxes(
        gt_bbox_for_matched_anchors, image_info[1])
    matched_gt_class_ids = matched_gt_class_ids[pos_idx].cpu().numpy()
    corner_anchors = output_handler._rescale_bboxes(corner_anchors, image_info[1])

    if model_outputs:
        test(raw_bbox=bbox_predictions, raw_class_values=classification_predictions, raw_class_ids=raw_class_ids,
             gt_bbox=gt_bbox, gt_class=gt_class,
             pred_bbox=prediction_bboxes, pred_class=predicted_classes,
             highest_confidence_for_predictions=highest_confidence_for_predictions,
             high_confidence_indeces=high_confidence_indeces,
             indeces_kept_by_nms=indeces_kept_by_nms,
             pos_idx=pos_idx,
             size=image_info[1],
             image=image,
             anchors=corner_anchors)

    return inspect_anchors(image=image, anchors=corner_anchors, gt_bbox_for_matched_anchors=gt_bbox_for_matched_anchors,
                    gt_classes_for_matched_anchors=matched_gt_class_ids, pos_idx=pos_idx, size=image_info[1],
                    visualize_anchors=visualize_anchors, visualize_anchor_gt_pair=visualize_anchor_gt_pair)

def test(raw_bbox=None, raw_class_values=None, raw_class_ids=None,
         gt_bbox=None, gt_class=None,
         pred_bbox=None, pred_class=None,
         highest_confidence_for_predictions=None,
         high_confidence_indeces=None,
         indeces_kept_by_nms=None,
         pos_idx=None, size=(320, 320),
         image=None, anchors=None,
         one_by_one=False):
    '''
    what we have:
    - raw bbox and class - all the model predictions (not filtered, not sorted, no nms) (values-confidences, ids-actual class ids)
    - gt_bbox and class - the ground truth for the image
    - pred_bbox and pred_class - sorted model predictions by confidence higher than a threshold
    - highest_confidence_for_predictions - what the maximum confidence for the respective prediction is
    - indeces of the highest confidence predictions (slice raw_bbox by this and get pred_bbox)
    - pos_idx - indeces of anchors (predictions) that mapped by IOU threshold (matching phase)
    - size - dimensions of image
    - image - actual input image
    - achors - corner format anchors
    '''
    matched_anchors = anchors[pos_idx]
    matched_bbox = raw_bbox[pos_idx]
    matched_conf = raw_class_values[pos_idx]
    matched_ids = raw_class_ids[pos_idx]

    # add the classes array for each bbox array
    print("GT BBOXES: ", gt_bbox, gt_bbox.shape)
    plot_bounding_boxes(image=image, bounding_boxes=gt_bbox, classes=gt_class, bbox_type="gt", message="Ground truth", size=size)

    print("Matched ANCHORS WITH THEIR RESPECTIVE OFFSET PREDICTIONS: ", matched_anchors, matched_anchors.shape)
    print("Matched Pred BBOXES: ", matched_bbox, matched_bbox.shape)
    print('CONFIDENCES FOR PREDICTED BBOXES that matched anchors: ', matched_conf)

    if one_by_one:
        for i in range(len(matched_anchors)):
            cur_anchor_bbox = matched_anchors[i]
            cur_pred_bbox = matched_bbox[i]
            cur_id = matched_ids[i]
            plot_bounding_boxes(image=image, bounding_boxes=cur_anchor_bbox, classes=cur_id, bbox_type="anchor", message="ANCHOR", size=size)
            plot_bounding_boxes(image=image, bounding_boxes=cur_pred_bbox, classes=cur_id, bbox_type="pred", message="PRED FROM ANCHOR", size=size)
            print('Confidence for this pair of anchor/pred: ',
                  matched_conf[i], size)
    else:
        plot_bounding_boxes(image=image, bounding_boxes=matched_anchors, classes=matched_ids, bbox_type="anchor", message="Anchors", size=size)
        plot_bounding_boxes(image=image, bounding_boxes=matched_bbox, classes=matched_ids, bbox_type="pred", message="Cheated Predictions", size=size)

    print("THIS IS PRED BBOX KEPT BY CONFIDENCE", pred_bbox, pred_bbox.shape)
    print("These are confidences for model outputs: ", highest_confidence_for_predictions)

    plot_bounding_boxes(image=image, bounding_boxes=pred_bbox, classes=pred_class, bbox_type="pred", message="Pre NMS Predictions", size=size)

    post_nms_predictions = pred_bbox[indeces_kept_by_nms]
    post_nms_classes = pred_class[indeces_kept_by_nms]
    plot_bounding_boxes(image=image, bounding_boxes=post_nms_predictions, classes=post_nms_classes, bbox_type="pred", message="Post NMS Predictions", size=size)
    print("THIS IS POST NMS PREDICTIONS", post_nms_predictions,
          post_nms_predictions.shape)
