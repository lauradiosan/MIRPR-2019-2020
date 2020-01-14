from train.helpers import *
from misc.postprocessing import *
from misc.utils import *

import numpy as np
import copy


class Model_output_handler():

    def __init__(self, conf_threshold=0.35, suppress_threshold=0.5):
        self.unnorm = UnNormalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
        self.confidence_threshold = conf_threshold
        self.suppress_threshold = suppress_threshold
        self.anchors_hw, self.grid_sizes = create_anchors()
        self.corner_anchors = hw2corners(self.anchors_hw[:, :2], self.anchors_hw[:, 2:])

    def process_outputs(self, bbox_predictions, classification_predictions, image_info):
        """
        returns complete model outputs in format array of:
        bbox, class id, confidence
        all operations done on cpu
        """
        prediction_bboxes, predicted_classes, highest_confidence_for_predictions, _ = self._get_sorted_predictions(
            bbox_predictions, classification_predictions, image_info)

        indeces_kept_by_nms = nms(prediction_bboxes, predicted_classes, self.suppress_threshold)

        # new structure: array of bbox, class, confidence
        # for some reason, bboxes should be WH format
        prediction_bboxes = corners_to_wh(prediction_bboxes)
        complete_outputs = np.concatenate(
            (prediction_bboxes, predicted_classes, highest_confidence_for_predictions), axis=1)

        return complete_outputs[indeces_kept_by_nms]

    def _unnorm_scale_image(self, image):
        """
        Args: image
        return: unnormalized numpy array as uint8
        """
        image = self.unnorm(image)
        image = (image * 255).cpu().numpy().astype(np.uint8)
        return image

    def _get_sorted_predictions(self, bbox_predictions, classification_predictions, image_info):
        """
        Returns the predicted bboxes, class ids and confidences sorted by confidence and above
        a given threshold
        """
        prediction_bboxes, prediction_confidences = self._convert_output_to_workable_data(
            bbox_predictions, classification_predictions, image_info[1])

        prediction_bboxes, prediction_confidences = self._predictions_over_threshold(
            prediction_bboxes, prediction_confidences)

        prediction_bboxes, predicted_classes, highest_confidence_for_predictions, high_confidence_indeces = self._sort_predictions_by_confidence(
            prediction_bboxes, prediction_confidences)

        highest_confidence_for_predictions = np.reshape(
            highest_confidence_for_predictions, (highest_confidence_for_predictions.shape[0], 1))

        return prediction_bboxes, predicted_classes, highest_confidence_for_predictions, high_confidence_indeces

    def _predictions_over_threshold(self, prediction_bboxes, predicted_confidences):
        """
        keep predictions above a confidence threshold
        """

        highest_confidence = np.amax(predicted_confidences, axis=1)
        keep_indices = (highest_confidence > self.confidence_threshold)

        prediction_bboxes = prediction_bboxes[keep_indices]
        predicted_confidences = predicted_confidences[keep_indices]

        return prediction_bboxes, predicted_confidences

    def _sort_predictions_by_confidence(self, prediction_bboxes, prediction_confidences):
        predicted_classes, highest_confidence_for_predictions = self._get_predicted_class(
            prediction_confidences)
        permutation = (-highest_confidence_for_predictions).argsort()

        highest_confidence_for_predictions = highest_confidence_for_predictions[permutation]
        prediction_bboxes = prediction_bboxes[permutation]
        predicted_classes = predicted_classes[permutation]

        return prediction_bboxes, predicted_classes, highest_confidence_for_predictions, permutation

    def _get_predicted_class(self, prediction_confidences):
        """
        returns class id and value of maximum confidence
        """
        predicted_idxs = np.argmax(prediction_confidences, axis=1)

        pos0 = (predicted_idxs == 0)
        pos1 = (predicted_idxs == 1)

        predicted_classes = np.zeros((predicted_idxs.shape[0], 1), dtype=np.int32)

        predicted_classes[pos0] = 1
        predicted_classes[pos1] = 3

        # predicted_classes = np.reshape(predicted_classes, (predicted_classes.shape[0], 1))

        highest_confidence_for_predictions = np.amax(prediction_confidences, axis=1)

        return predicted_classes, highest_confidence_for_predictions

    def _convert_bboxes_to_workable_data(self, prediction_bboxes, size):
        height, width = size
        prediction_bboxes = prediction_bboxes.cpu()
        prediction_bboxes = activations_to_bboxes(
            prediction_bboxes, self.anchors_hw, self.grid_sizes)
        return self._rescale_bboxes(prediction_bboxes, size)

    def _convert_confidences_to_workable_data(self, prediction_confidences):
        return prediction_confidences.sigmoid().cpu().numpy()

    def _convert_output_to_workable_data(self, model_output_bboxes, model_output_confidences, size):
        prediction_bboxes = self._convert_bboxes_to_workable_data(
            model_output_bboxes, size)
        prediction_confidences = self._convert_confidences_to_workable_data(
            model_output_confidences)
        return prediction_bboxes, prediction_confidences

    def _rescale_bboxes(self, bboxes, size):
        """
        Args: array of bboxes in corner format
        returns: bboxes upscaled by height and width as numpy array on cpu
        """
        height, width = size
        scale_bboxes = copy.deepcopy(bboxes)
        scale_bboxes[:, 0] *= height
        scale_bboxes[:, 2] *= height
        scale_bboxes[:, 1] *= width
        scale_bboxes[:, 3] *= width
        return (scale_bboxes.cpu().numpy()).astype(int)


class UnNormalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, tensor):
        """
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
        Returns:
            Tensor: Normalized image.
        """
        for t, m, s in zip(tensor, self.mean, self.std):
            t.mul_(s).add_(m)
            # The normalize code -> t.sub_(m).div_(s)
        return tensor
