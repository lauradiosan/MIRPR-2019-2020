from classify import update
from config import *
from fill_db_with_slots import fill_db
from get_test_results import get_test_results

if __name__ == "__main__":
    global test_dataset, test_boxes, db_path
    fill_db(db_path, test_dataset + test_boxes)

    # specify path to the model you want to test
    update("CNNTensorflow/model.h5", db_path)

    get_test_results()
