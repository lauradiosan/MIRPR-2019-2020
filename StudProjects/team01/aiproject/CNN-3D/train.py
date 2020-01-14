# Some links.
# a deep dream of a NN - https://www.youtube.com/watch?v=sh-MQboWJug

import tensorflow as tf
import pickle
import nibabel as nib
import matplotlib.pyplot as plt
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from nibabel.testing import data_path
from process_data import *

# Create and save the training and testing data.
create_training_data()
save_data()

# Get the training and testing data.
(train_images, train_labels), (test_images, test_labels) = load_data()

train_images, test_images = train_images / 255.0, test_images / 255.0     # normalize data

class_names = ['HCM', 'NOR', 'DCM', 'MINF', 'RV']

# Create the model. 
model = Sequential()

model.add(Conv2D(32, (3, 3), activation = 'relu', input_shape = train_images.shape[1:]))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(Flatten())

model.add(Dense(64, activation = 'relu'))
model.add(Dense(10, activation = 'softmax'))

# model.summary()

model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])

# Train and save the trained model.
# model_path = "savedModels\\model"
# history = model.fit(
#         train_images, train_labels, 
#         nb_epoch = 3,
#         validation_data = (test_images, test_labels), 
#         verbose = 1, 
#         callbacks = [
#             ModelCheckpoint(
#                 filepath = model_path + '-{epoch:02d}-{val_accuracy:.2f}.hdf5',
#                 save_best_only = True, 
#                 monitor = 'val_accuracy', 
#                 verbose = 1
#                 ),
#             ReduceLROnPlateau(
#                 monitor = 'val_accuracy', 
#                 factor = 0.5, 
#                 patience = 10, 
#                 min_delta = 0.01,
#                 verbose = 1
#                 )
#         ]
#     )

# Train the model without saving it
history = model.fit(
            train_images, train_labels, 
				    epochs = 5,
            validation_data = (test_images, test_labels)
          )

test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose = 3)

print("---> test_accuracy: ")              # printing the results of the training (accuracy and loss)
print(test_accuracy)
print("---> test_loss: ")
print(test_loss)


def get_prediction(img_path):
  '''
  Returns the prediction of a nifty image. 
  
  Parameters
  ----------
    - img_path: string 
        Path of the image.
  Returns
  ----------
    - string
        The predicted label based on the trained model.
  '''
  model.load_weights("savedModels/model-01-1.00.hdf5")
  img_nii = nib.load(img_path)
  img_array = np.array(img_nii.dataobj)
  new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
  arr = np.array(new_array).reshape(-1,IMG_SIZE,IMG_SIZE,10)
  pickle_out = open("XT.pickle", "wb")
  pickle.dump(arr, pickle_out)
  pickle_out.close()
  test = pickle.load(open("XT.pickle", "rb"))
  t = np.array(test)
  t = t / 255.0
  m = model.predict_classes(t)

  return class_names[m[0]]
