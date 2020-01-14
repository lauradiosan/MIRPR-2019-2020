import tensorflow as tf
import os

from keras.optimizers import Adam
from keras_preprocessing.image import ImageDataGenerator
from keras.models import load_model

num_classes = 7
img_rows, img_cols = 48, 48
batch_size = 100

train_data_dir = '../res/Training'
validation_data_dir = '../res/PublicTest'

val_datagen = ImageDataGenerator(rescale=1. / 255)
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=20,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode='nearest')
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(48, 48),
    batch_size=batch_size,
    color_mode="grayscale",
    class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(48, 48),
    batch_size=batch_size,
    color_mode="grayscale",
    class_mode='categorical')

model = load_model("../res/fer/trained_model_resnet_improved.hdf5")
model.summary()

filepath = os.path.join("../res/fer/trained_model_resnet_improving.hdf5")

checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath,
                                                monitor='val_accuracy',
                                                save_best_only=True,
                                                mode='max')
callbacks = [checkpoint]
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.00005, decay=1e-4), metrics=['accuracy'])
nb_train_samples = 28709
nb_validation_samples = 3589
epochs = 30
model_info = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    verbose=1,
    callbacks=callbacks,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)
