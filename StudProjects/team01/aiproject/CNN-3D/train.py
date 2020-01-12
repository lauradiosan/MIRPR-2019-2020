# Some links.
# a deep dream of a NN - https://www.youtube.com/watch?v=sh-MQboWJug

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
import nibabel as nib
from nibabel.testing import data_path
import matplotlib.pyplot as plt
import cv2
import numpy as np
from process_data import *


create_training_data()
save_data()
(train_images, train_labels), (test_images, test_labels) = load_data()

train_images, test_images = train_images / 255.0, test_images / 255.0

class_names = ['HCM', 
		       'NOR','DCM']

model = Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=train_images.shape[1:]))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())

model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))

# model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, 
				    epochs=5 ,
                    validation_data=(test_images, test_labels)
                    )
def get_prediction(img_path):
    img_nii = nib.load(img_path)
    img_array = np.array(img_nii.dataobj)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    arr=np.array(new_array).reshape(-1,IMG_SIZE,IMG_SIZE,10)
    pickle_out = open("XT.pickle", "wb")
    pickle.dump(arr, pickle_out)
    pickle_out.close()
    test = pickle.load(open("XT.pickle", "rb"))
    t = np.array(test)
    t=t/255.0
    m=model.predict_classes(t)
    return class_names[m[0]]
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=20)
#print(test_loss)
#print(" ")
#print(test_acc)