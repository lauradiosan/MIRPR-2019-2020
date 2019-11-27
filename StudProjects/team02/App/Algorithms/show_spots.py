from tinydb import TinyDB, Query

from config import *
import cv2


def show_spots(path):
	"""
	Show classification results for a single image
	:param path:
	:return:
	"""
	global db_path
	db = TinyDB(db_path)
	q = Query()

	img = cv2.imread(path)

	cv2.namedWindow('image')

	spots = db.search(q.url == path)[0]['spots']
	for spot in spots:
		if spot["occupied"]:
			# create red box
			cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]), (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 0, 255), 2)
		else:
			# create green box
			cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]), (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 255, 0), 2)

	cv2.imshow('image', img)
	cv2.waitKey(0)


if __name__ == "__main__":
	show_spots("test_dataset\\S\\2015-11-12_0713.jpg")
