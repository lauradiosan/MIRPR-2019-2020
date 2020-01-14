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

model = Sequential()

num_features = 64
num_labels = 7
batch_size = 128
epochs = 40
width, height = 96, 96

model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu', input_shape=(96, 96, 1), data_format='channels_last', kernel_regularizer=l2(0.01)))
model.add(BatchNormalization(name='lol'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='blabla'))


# load the pretrained model
prior = load_model('model/model_fer.h5')
MODELPATH = './model/model_fer_resized.h5'

# add all but the first two layers of VGG16 to the new model
# strip the input layer out, this is now 96x96
# also strip out the first convolutional layer, this took the 48x48 input and convolved it but
# this is now the job of the three new layers.
# for layer in prior.layers[0].layers[2:]:
    # model.add(layer)

model.summary()
prior.summary()

# re-add the feedforward layers on top
for layer in prior.layers[1:]:
    layer.trainable = False
    model.add(layer)

model.summary()

# the pretrained CNN layers are already marked non-trainable
# mark off the top layers as well
# for layer in prior.layers[-4:]:
    # layer.trainable = False
    
# compile the model
model.compile(
    optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

train_datagen = ImageDataGenerator()

test_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
        'aug_data/train',
        target_size=(96, 96),
        batch_size=128,
        class_mode='categorical',
        shuffle=True,
        color_mode='grayscale')

validation_generator = test_datagen.flow_from_directory(
        'aug_data/validation',
        target_size=(96, 96),
        batch_size=1,
        class_mode='categorical',
        color_mode='grayscale')

lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=0.90, patience=4, verbose=1)

early_stopper = EarlyStopping(monitor='val_loss', min_delta=0, patience=4, verbose=1, mode='auto')

checkpointer = ModelCheckpoint(MODELPATH, monitor='val_loss', verbose=1, save_best_only=True)

model.fit_generator(train_generator,
          epochs=epochs,
          verbose=1,
          validation_data=validation_generator,
          shuffle=True,
          steps_per_epoch=159, #dataset size/ batch size
          callbacks=[early_stopper, lr_reducer, checkpointer])