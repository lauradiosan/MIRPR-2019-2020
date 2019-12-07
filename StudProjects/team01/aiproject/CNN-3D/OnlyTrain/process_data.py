# Useful stuff that I wish I knew 3 days ago
# Documentation nibabel - https://nipy.org/nibabel/nibabel_images.html
# Some tutorial for preparing custom data for CNN - https://www.youtube.com/watch?v=j-3vuBynnOE&list=PLQVvvaa0QuDfhTox0AjmQ6tvTgMBZBEXN&index=2
# Some tutorial for CNN - https://www.youtube.com/watch?v=WvoLTXIjBYU&list=PLQVvvaa0QuDfhTox0AjmQ6tvTgMBZBEXN&index=3

import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path
import matplotlib.pyplot as plt
import cv2
import random
import pickle


DATADIR = "simple_data"
CATEGORIES = ["HCM", "NOR","DCM"]
IMG_SIZE = 256

training_data = []

def create_training_data():
	for category in CATEGORIES:
		path = os.path.join(DATADIR, category)
		class_num = CATEGORIES.index(category)
		for img in os.listdir(path):
			try:
				img_path = os.path.join(path, img)
				img_nii = nib.load(img_path)
				img_array = np.array(img_nii.dataobj)
				new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
				training_data.append([new_array, class_num])
			except Exception as e:
				print("=== Ai o exceptie - ", e)
	random.shuffle(training_data)

def save_data():
	X = []
	y = []

	for features, label in training_data:
		X.append(features)
		y.append(label)


	X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 10)

	pickle_out = open("X.pickle", "wb")
	pickle.dump(X, pickle_out)
	pickle_out.close()

	pickle_out = open("y.pickle", "wb")
	pickle.dump(y, pickle_out)
	pickle_out.close()

def load_data():
	train_images = pickle.load(open("X.pickle", "rb")) 
	train_labels = pickle.load(open("y.pickle", "rb")) 
	test_images = pickle.load(open("X.pickle", "rb")) 
	test_labels = pickle.load(open("y.pickle", "rb"))

	train_images = np.array(train_images)
	train_labels = np.array(train_labels)
	test_images = np.array(test_images)
	test_labels = np.array(test_labels)

	train_labels = train_labels.reshape((len(train_labels), 1))
	test_labels = test_labels.reshape((len(test_labels), 1))
	
	return (train_images, train_labels), (test_images, test_labels)


create_training_data()
save_data()