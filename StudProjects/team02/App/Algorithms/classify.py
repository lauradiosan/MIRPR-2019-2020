from tinydb import TinyDB, Query
from CNNTensorflow.utils import img_to_array
from PIL import Image
from config import *

import tensorflow as tf
import numpy as np
import time


def crop_img(img, crop_data):
    """
    Crop parking spot out of full-size image
    """
    global width, height
    x = crop_data[0]
    y = crop_data[1]
    w = crop_data[2]
    h = crop_data[3]
    cropped_img = img.crop((x, y, x + w, y + h))

    new_size = (width, height)
    cropped_img = cropped_img.resize(new_size)

    return cropped_img


def update(model_path, db_path):
    """
    Update data for all parking spots in the db
    """
    db = TinyDB(db_path)
    parkings = db.all()

    all_images_proc_time = 0
    for parking in parkings:
        global test_dataset, weather_sunny
        camera_image = Image.open(test_dataset + weather_sunny + parking['url'])

        print('processing image ' + parking['url'])

        # Process each parking spot
        parking_spots = parking['spots']
        updated_parking_spots = []

        single_img_proc_time = 0
        model = tf.keras.models.load_model(model_path)
        for spot in parking_spots:

            spot_image = crop_img(camera_image, spot['crop'])
            spot_image = img_to_array(spot_image, path=False)
            
            start = time.time()
            prediction = model.predict(np.array([spot_image]))
            end = time.time()
            if prediction[0][0] > prediction[0][1]:
                spot['occupied'] = False
            else:
                spot['occupied'] = True
            updated_parking_spots.append(spot)

            # tf.keras.backend.clear_session()
            print(str(end-start))
            single_img_proc_time += end-start
        tf.keras.backend.clear_session()
        all_images_proc_time += single_img_proc_time
        print("Total processing time: " + str(single_img_proc_time))
        db.update({'spots': updated_parking_spots}, eids=[parking.eid])

    print("Average processing time per image: " + str(all_images_proc_time / len(parkings)))


if __name__ == "__main__":
    global db_path, model_path
    update(model_path, db_path)
