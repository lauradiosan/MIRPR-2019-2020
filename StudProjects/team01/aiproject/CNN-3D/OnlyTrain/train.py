# Some links.
# a deep dream of a NN - https://www.youtube.com/watch?v=sh-MQboWJug

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
from process_data import load_data

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

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=3)

print(test_acc)