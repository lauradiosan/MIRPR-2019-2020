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

            crop_arr = [int(row["X"]), int(row["Y"]), int(row["W"]), int(row["H"])]
            custom_dict = dict()
            custom_dict["slot_id"] = row["SlotId"]
            custom_dict["position"] = [int(row["Row"]), int(row["Col"])]
            custom_dict["crop"] = crop_arr
            custom_dict["occupied"] = False
            spots.append(custom_dict)
            line_count += 1

    test_images = ["frame.png"]
    for img_url in test_images:
        db.insert({"url": img_url, "spots": spots})

    db.close()


if __name__=="__main__":
    fill_db("db.json", "boxes.csv")