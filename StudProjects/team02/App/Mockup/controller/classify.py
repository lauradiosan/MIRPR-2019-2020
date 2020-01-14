from tinydb import TinyDB, Query
#from utils import img_to_array
from PIL import Image
import cv2
from controller.config import *
from controller.models import get_cnn_model, get_vgg_model
from controller.utils import img_to_array

import numpy as np
import tensorflow as tf
import time

def crop_img(img, crop_data):
    """
    Crop parking spot out of full-size image
    """
    x = crop_data[0]
    y = crop_data[1]
    w = crop_data[2]
    h = crop_data[3]
    cropped_img = img.crop((x, y, x + w, y + h))

    new_size = (width, height)
    cropped_img = cropped_img.resize(new_size)

    return cropped_img

def get_crop_area(spot):
    left_corner_x = int(spot['crop'][0])
    left_corner_y = int(spot['crop'][1])
    right_corner_x = int(spot['crop'][2])
    right_corner_y = int(spot['crop'][3])

    return [left_corner_x, left_corner_y, right_corner_x, right_corner_y]

def predict_vgg(image):
    model = get_vgg_model()
    prediction = model.predict(image)
    if round(prediction[0][0]) is 1:
        return True
    return False

def predict_cnn(image):
    model = get_cnn_model()
    prediction = model._model.predict(image)
    if prediction[0][0] > prediction[0][1]:
        return False
    return True

def predict(db_path, image):
    db = TinyDB(db_path)
    parkings = db.all()
    for parking in parkings:
        parking_spots = parking['spots']
        updated_parking_spots = []
        for spot in parking_spots:
            crop_area = get_crop_area(spot)
            spot_image = crop_img(image, crop_area)
            spot_image_array = img_to_array(spot_image, path=False)
            spot['occupied'] = predict_cnn(np.array([spot_image_array]))
            updated_parking_spots.append(spot)
        tf.keras.backend.clear_session()
        db.update({'spots': updated_parking_spots}, eids=[parking.eid])
    draw_all_boxes()

def draw_all_boxes():
    db = TinyDB(db_path)
    parkings = db.all()
    for parking in parkings:
        img_url = 'frame.png'
        draw_boxes_for_image(img_url)


def draw_boxes_for_image(img_path):
    """
    Draw a box around each parking spot from a full image: green for free, red for occupied
    """

    global test_dataset
    full_path = 'frame.png'
    img = image = cv2.imread(full_path)

    global db_path
    db = TinyDB(db_path)
    q = Query()
    spots = db.search(q.url == img_path)[0]['spots']
    for spot in spots:
        crop = get_crop_area(spot)
        color = (0, 255, 0)
        if spot["occupied"]:
            color = (0, 0, 255)

        cv2.rectangle(img, (crop[0], crop[1]),
                        (crop[0] + crop[2], crop[1] + crop[3]), color, 2)

    global test_output
    output_path = 'prediction.png'
    cv2.imwrite(output_path, img)


if __name__ == "__main__":
    global db_path, model_path
    update(db_path)
    draw_all_boxes()
