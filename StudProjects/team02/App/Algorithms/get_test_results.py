import cv2
from tinydb import TinyDB, Query
from config import *

global db_path
db = TinyDB(db_path)


def read_test_labels():
    """
    Read the file containing labels for the test images
    :return: dictionary of type (slot -> occupancy)
    """
    print("reading labels")
    global test_dataset, test_labels
    labels_path = test_dataset + test_labels
    labels_dict = {}
    with open(labels_path, 'r') as lbl_file:
        line = lbl_file.readline()
        while(line):
            line = line.strip().split(" ")
            labels_dict[line[0][25:-4]] = int(line[1])
            line = lbl_file.readline()
    return labels_dict


def draw_boxes_for_image(img_path):
    """
    Draw a box around each parking spot from a full image: green for free, red for occupied
    """
    global test_dataset, weather_sunny
    full_path = test_dataset + weather_sunny + img_path
    img = image = cv2.imread(full_path)

    global db_path
    db = TinyDB(db_path)
    q = Query()
    spots = db.search(q.url == img_path)[0]['spots']
    for spot in spots:
        if spot["occupied"]:
            # create red box
            cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]),
                          (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 0, 255), 2)
        else:
            # create green box
            cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]),
                          (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 255, 0), 2)

    global test_output
    output_path = test_output + img_path
    cv2.imwrite(output_path, img)


def get_test_results():
    """
    Read test classification results and calculate accuracy
    """
    test_labels = read_test_labels()
    parkings = db.all()
    accuracies = {}

    for parking in parkings:
        weather = parking['weather']
        img_url = parking['url']
        all_spots = parking['spots']

        img_guessed = 0
        for spot in all_spots:
            label_key = weather + '_' + img_url[:13] + '.' + img_url[13:15] + '_C08_' +  spot['slot_id']

            expected_label = test_labels[label_key]
            actual_label = spot['occupied']
            if bool(expected_label) == actual_label:
                img_guessed += 1
        
        accuracies[img_url] = img_guessed/len(all_spots)
        draw_boxes_for_image(img_url)

    average_accuracy = sum(list(accuracies.values())) / len(list(accuracies.values()))
    print("The average accuracy (% of correctly classified spots in a full image) is " + str(round(average_accuracy, 4)))


if __name__ == "__main__":
    get_test_results()

            





