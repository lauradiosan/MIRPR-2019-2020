from misc.metrics import get_predicted_class, sort_predictions_by_confidence, get_IoU, get_intersection, help_calculate_AP
import numpy as np


def test_get_predicted_class():
    # TEST 1
    test1 = np.array([[0.4, 0.6], [0.1, 0.7], [0.8, 0.001]])

    predicted_classes_1, highest_confidence_for_each_prediction_1 = get_predicted_class(test1)

    correct_predicted_classes_1 = np.array([1, 1, 0])
    correct_highest_confidence_for_each_prediction_1 = np.array([0.6, 0.7, 0.8])

    print(predicted_classes_1)

    assert np.array_equal(predicted_classes_1, correct_predicted_classes_1) is True
    assert np.allclose(highest_confidence_for_each_prediction_1,
                       correct_highest_confidence_for_each_prediction_1) is True

    # TEST 2

    test2 = np.array([[0.4, 0.6], [0.1, 0.7], [0.8, 0.001], [0.004123, 0.012345]])

    predicted_classes_2, highest_confidence_for_each_prediction_2 = get_predicted_class(test2)

    correct_predicted_classes_2 = np.array([1, 1, 0, 1])
    correct_highest_confidence_for_each_prediction_2 = np.array([0.6, 0.7, 0.8, 0.012345])

    assert np.array_equal(predicted_classes_2, correct_predicted_classes_2) is True
    assert np.allclose(highest_confidence_for_each_prediction_2,
                       correct_highest_confidence_for_each_prediction_2) is True

    print("TESTELE PENTRU FUNCTIA get_predicted_class() AU TRECUT CU SUCCES")


def test_sort_predictions_by_confidence():
    # TEST 1

    test_bboxes_1 = np.array([[1, 1], [2, 2]])
    test_predicted_classes_1 = np.array([0, 0])
    test_highest_confidence_for_prediction_1 = np.array([0.5, 0.4])

    test_bboxes_1, test_predicted_classes_1, test_highest_confidence_for_prediction_1 = sort_predictions_by_confidence(
        test_bboxes_1, test_predicted_classes_1, test_highest_confidence_for_prediction_1)

    assert np.array_equal(test_bboxes_1, np.array([[1, 1], [2, 2]])) is True
    assert np.array_equal(test_predicted_classes_1, np.array([0, 0])) is True
    assert np.allclose(test_highest_confidence_for_prediction_1, np.array([0.5, 0.4])) is True

    # TEST 2

    test_bboxes_2 = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]])
    test_predicted_classes_2 = np.array([0, 0, 1, 0, 1, 1])
    test_highest_confidence_for_prediction_2 = np.array(
        [0.5, 0.4, 0.000436, 0.960541, 0.124563, 0.77777])

    test_bboxes_2, test_predicted_classes_2, test_highest_confidence_for_prediction_2 = sort_predictions_by_confidence(
        test_bboxes_2, test_predicted_classes_2, test_highest_confidence_for_prediction_2)

    assert np.array_equal(test_bboxes_2, np.array(
        [[4, 4], [6, 6], [1, 1], [2, 2], [5, 5], [3, 3]])) is True
    assert np.array_equal(test_predicted_classes_2, np.array([0, 1, 0, 0, 1, 1])) is True
    assert np.allclose(test_highest_confidence_for_prediction_2, np.array(
        [0.960541, 0.77777, 0.5, 0.4, 0.124563, 0.000436])) is True

    print("TESTELE PENTRU FUNCTIA sort_predictions_by_confidence() AU TRECUT CU SUCCES")


def test_get_IoU():
    bbox_1 = np.array([0, 0, 50, 50])
    bbox_2 = np.array([0, 0, 100, 100])

    assert get_IoU(bbox_1, bbox_2) == 0.25

    print("TESTELE PENTRU FUNCTIA get_IoU() AU TRECUT CU SUCCES")


def test_get_intersection():
    # TEST 1

    bbox_1 = np.array([0, 0, 50, 50])
    bbox_2 = np.array([0, 0, 100, 100])

    intersection = get_intersection(bbox_1, bbox_2)

    assert np.array_equal(intersection, np.array([0, 0, 50, 50]))

    # TEST 2

    bbox_1 = np.array([36, 22, 50, 50])
    bbox_2 = np.array([20, 30, 79, 100])

    intersection = get_intersection(bbox_1, bbox_2)

    assert np.array_equal(intersection, np.array([36, 30, 50, 50]))

    print("TESTELE PENTRU FUNCTIA get_intersection() AU TRECUT CU SUCCES")


def test_help_calculate_AP():
    # TEST 1

    gt_bboxes = np.array([[25, 25, 100, 100], [15, 15, 20, 20]])
    gt_classes = np.array([0, 1])

    prediction_bboxes = np.array([[25, 25, 100, 100], [15, 15, 20, 20]])
    prediction_confidences = np.array([[0.6, 0.2], [0.2, 0.8]])

    precision = help_calculate_AP(
        gt_bboxes, gt_classes, prediction_bboxes, prediction_confidences, 0.5)

    assert precision == 1

    # TEST 2

    gt_bboxes = np.array([[25, 25, 100, 100], [15, 15, 20, 20]])
    gt_classes = np.array([0, 1])

    prediction_bboxes = np.array([[25, 25, 100, 100], [18, 18, 20, 20]])
    prediction_confidences = np.array([[0.6, 0.2], [0.2, 0.8]])

    precision = help_calculate_AP(
        gt_bboxes, gt_classes, prediction_bboxes, prediction_confidences, 0.5)

    assert precision == 0.5

    # TEST 3

    gt_bboxes = np.array([[25, 25, 100, 100]])
    gt_classes = np.array([0])

    prediction_bboxes = np.array([[25, 25, 100, 100]])
    prediction_confidences = np.array([[0.6, 0.2]])

    precision = help_calculate_AP(
        gt_bboxes, gt_classes, prediction_bboxes, prediction_confidences, 0.5)

    assert precision == 1

    # TEST 4

    gt_bboxes = np.array([[25, 25, 100, 100]])
    gt_classes = np.array([0])

    prediction_bboxes = np.array([[25, 25, 100, 100]])
    prediction_confidences = np.array([[0.2, 0.6]])

    precision = help_calculate_AP(
        gt_bboxes, gt_classes, prediction_bboxes, prediction_confidences, 0.5)

    assert precision == 0

    # TEST 5

    gt_bboxes = np.array([[25, 25, 100, 100], [15, 15, 20, 20]])
    gt_classes = np.array([0, 0])

    prediction_bboxes = np.array([[25, 25, 100, 100], [18, 18, 20, 20]])
    prediction_confidences = np.array([[0.6, 0.2], [0.3, 0.8]])

    precision = help_calculate_AP(
        gt_bboxes, gt_classes, prediction_bboxes, prediction_confidences, 0.5)

    assert precision == 0.5

    print("TESTELE PENTRU FUNCTIA help_calculate_AP() AU TRECUT CU SUCCES")


def run():
    test_get_predicted_class()
    test_sort_predictions_by_confidence()
    test_get_IoU()
    test_get_intersection()
    test_help_calculate_AP()
