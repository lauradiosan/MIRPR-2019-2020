# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adagrad
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau, TensorBoard, EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

MODELPATH = './model/model.h5'
num_features = 64
num_labels = 7
batch_size = 128
epochs = 40
width, height = 64, 64

model = Sequential()

model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu', input_shape=(width, height, 1), data_format='channels_last', kernel_regularizer=l2(0.01)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(2*2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(2*2*2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(2*2*2*num_features, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(2*2*num_features, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(2*num_features, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(num_features, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(num_labels, activation='softmax'))

model.summary()

def standardize(image):
    return (image - image.mean()) / (image.std() + 1e-8)


train_datagen = ImageDataGenerator(
        # rotation_range=0.2,
        # preprocessing_function=standardize
        )

test_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
        'aug_data/train',
        target_size=(width, height),
        batch_size=128,
        class_mode='categorical',
        shuffle=True,
        color_mode='grayscale')

validation_generator = test_datagen.flow_from_directory(
        'aug_data/validation',
        target_size=(width, height),
        batch_size=1,
        class_mode='categorical',
        color_mode='grayscale')


model.compile(
        loss=categorical_crossentropy,
        optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
        # optimizer=Adagrad(),
        # optimizer=RMSprop(learning_rate=0.001, rho=0.9),
        metrics=['accuracy'])

lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=0.90, patience=3, verbose=1)

early_stopper = EarlyStopping(monitor='val_loss', min_delta=0, patience=4, verbose=1, mode='auto')

checkpointer = ModelCheckpoint(MODELPATH, monitor='val_loss', verbose=1, save_best_only=True)

model.fit_generator(train_generator,
          epochs=epochs,
          verbose=1,
          validation_data=validation_generator,
          shuffle=True,
          steps_per_epoch=159, #dataset size/ batch size
          callbacks=[early_stopper, lr_reducer, checkpointer])

model.save("model_la_final.h5")
print("Saved model to disk")

