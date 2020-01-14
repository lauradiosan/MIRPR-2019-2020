import torch
from torch import nn
import numpy as np
import random

from train.helpers import *
from misc.postprocessing import *


# inspired by fastai course
class BCE_Loss(nn.Module):
    def __init__(self, n_classes, device):
        super().__init__()
        self.n_classes = n_classes
        self.device = device
        self.id2idx = {1: 0, 3: 1}

    def forward(self, pred, targ, norm_factor):
        '''
        Arguments:
            pred - tensor of shape anchors x n_classes
            targ - tensor of shape anchors

        Explanation: computes weighted BCE loss between model prediction and target
            model predicts scores for each class, all 0s means background

        Returns: total loss averaged by the numbers of mathced anchors (due to focall los, it is  presumed
        backgrounds contribute little)
        '''
        t = []
        targ = targ.cpu().numpy()
        for clas_id in targ:
            bg = [0] * self.n_classes
            if clas_id != 100:
                bg[self.id2idx[clas_id]] = 1
            t.append(bg)

        t = torch.FloatTensor(t).to(self.device)
        weight = self.get_weight(pred, t)
        return torch.nn.functional.binary_cross_entropy_with_logits(pred, t, weight=weight,
                                                                    size_average=None, reduce=None, reduction='sum') / norm_factor

    def get_weight(self, x, t):
        # focal loss decreases loss for correctly classified (P>0.5) examples, relative to the missclassified ones
        # thus increasing focus on them
        alpha, gamma = 0.25, 2.
        p = x.detach().sigmoid()

        # focal loss factor - decreases relative loss for well classified examples
        pt = p*t + (1-p)*(1-t)

        # counter positive/negative examples imbalance by assigning higher relative values to positives=1
        w = alpha*t + (1-alpha)*(1-t).to(self.device)

        # these two combined strongly encourage the network to predict a high value when
        # there is indeed a positive example
        return w * ((1-pt).pow(gamma))


class Detection_Loss():
    """
    Computes both localization and classification loss

    in args:
    anchors - #anchors x 4 cuda tensor
    grid_sizes - #anchors x 1 cuda tensor
    """

    def __init__(self, anchors, grid_sizes, device, params):
        self.anchors = anchors
        self.grid_sizes = grid_sizes
        self.device = device
        self.params = params
        self.class_loss = BCE_Loss(params.n_classes, self.device)

    def ssd_1_loss(self, pred_bbox, pred_class, gt_bbox, gt_class):
        """
        Arguments:
            pred_bbox - #anchors x 4 cuda tensor - predicted bboxes for current image
            pred_class - #anchors x 2 cuda tensor - predicted class confidences for cur img
            gt_bbox - #obj x 4 cuda tensor - GT bboxes for objects in the cur img
            gt_class - #obj x 1 cuda tensor - class IDs for objects in cur img

        Explanation:
        model outputs offsets are converted to the final bbox predictions
        the matching phase is carried out
        localization (L1) and classification (BCE) loss are being computed and returned
        """
        # make network outputs same as gt bbox format
        pred_bbox = activations_to_bboxes(pred_bbox, self.anchors, self.grid_sizes)

        # compute IOU for obj x anchor
        overlaps = jaccard(gt_bbox, hw2corners(self.anchors[:, :2], self.anchors[:, 2:]))

        # map each anchor to the highest IOU obj, gt_idx - ids of mapped objects
        gt_bbox_for_matched_anchors, matched_gt_class_ids, pos_idx = map_to_ground_truth(
            overlaps, gt_bbox, gt_class, self.params)

        loc_loss = ((pred_bbox[pos_idx] - gt_bbox_for_matched_anchors).abs()).mean()

        class_loss = self.class_loss(pred_class, matched_gt_class_ids, pos_idx.shape[0])
        return loc_loss, class_loss

    def ssd_loss(self, pred, targ):
        """
        Arguments:
            pred - model output - two tensors of dim B x #anchors x 4 and B x #anchors x n_classes in a list
            targ - ground truth - two tensors of dim B x #obj x 4 and B x #obj in a list

        Explanation:
        Loss will be calculated per image in the batch
        anchors will be mappend to overlapping GT bboxes higher than a threshold
        feature map cells corresponding to those anchors will have to predict those gt bboxes (loc loss)
        all feature map cells hape to predict a confidence (class loss)

        Return: loc and class loss per whole batch
        """

        localization_loss, classification_loss = 0., 0.

        for idx in range(pred[0].shape[0]):
            pred_bbox, pred_class = pred[0][idx], pred[1][idx]
            gt_bbox, gt_class = targ[0][idx].to(self.device), targ[1][idx].to(self.device)

            l_loss, c_loss = self.ssd_1_loss(pred_bbox, pred_class, gt_bbox, gt_class)
            localization_loss += l_loss
            classification_loss += c_loss

        return localization_loss, classification_loss
