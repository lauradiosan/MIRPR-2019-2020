from tinydb import TinyDB
import csv
import os
from config import *


def fill_db(db_path, csv_path):
    """
    Read parking slot data from the csv file and build the database
    """
    db = TinyDB(db_path)

    with open(csv_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0

        spots = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            crop_arr = [int(int(row["X"]) / 2.6) , int(int(row["Y"]) / 2.6), int(int(row["W"]) / 2.6), int(int(row["H"]) / 2.6)]
            custom_dict = dict()
            custom_dict["slot_id"] = row["SlotId"]
            custom_dict["crop"] = crop_arr
            custom_dict["occupied"] = False
            spots.append(custom_dict)
            line_count += 1

    global test_dataset, weather_sunny
    test_images = os.listdir(test_dataset + weather_sunny)
    for img_url in test_images:
        db.insert({"weather": "S", "url": img_url, "spots": spots})

    db.close()


if __name__=="__main__":
    global test_dataset, test_boxes, db_path
    fill_db(db_path, test_dataset + test_boxes)