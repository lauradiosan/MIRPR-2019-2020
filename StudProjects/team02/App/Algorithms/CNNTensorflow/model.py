import os
import numpy as np
import tensorflow as tf
from utils import img_to_array, unison_shuffled_copies
from config import *


def load_images(dataset_location):
	"""
	Prepare dataset for training
	"""
	global label_free, label_occupied
	samples_free = dataset_location + label_free
	samples_occupied = dataset_location + label_occupied

	images_free = os.listdir(samples_free)
	images_occupied = os.listdir(samples_occupied)
	global dataset_size, width, height, channels
	data_x = np.ndarray(shape=(dataset_size, width, height, channels), dtype=np.float32)
	data_y = np.ndarray(shape=(dataset_size), dtype=np.float32)

	i = 0
	errors = 0
	for img in images_free:
		img_path = samples_free + img

		try:
			img_arr = img_to_array(img_path)
			data_x[i] = img_arr
			data_y[i] = 0.
			i += 1
			print(i)
		except ValueError as e:
			print(e)
			print(img, '<--- Does not work')
			errors += 1
		if i == dataset_size / 2:
			break

	# Images containing occupied parking spots
	for img in images_occupied:
		img_path = samples_occupied + img

		try:
			img_arr = img_to_array(img_path)
			data_x[i] = img_arr
			data_y[i] = 1.
			i += 1
			print(i)
		except ValueError:
			print(img, '<--- Does not work')
			errors += 1
		if i == dataset_size:
			break

	data_x = np.array(data_x)
	data_y = np.array(data_y)

	if errors != 0:
		data_x = data_x[:-errors]
		data_y = data_y[:-errors]

	data_x, data_y = unison_shuffled_copies(data_x, data_y)

	return data_x, data_y


def train():
	global train_dataset
	data_x, data_y = load_images(train_dataset)
	
	model = tf.keras.models.Sequential([
		tf.keras.layers.Convolution2D(32, 5, 5, input_shape=(width, height, 3), activation=tf.nn.relu),
		tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
		tf.keras.layers.Flatten(),
		tf.keras.layers.Dense(512, activation=tf.nn.relu),
		tf.keras.layers.Dense(2, activation=tf.nn.softmax)
	])

	model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
	print('Training model...')
	model.fit(data_x, data_y, validation_split=0.33, epochs=5)
	model.save('model.h5')
