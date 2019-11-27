# Set tensorflow backend to use only required GPU memory
import cv2
import tensorflow as tf
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Model, Sequential, model_from_json, load_model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator,img_to_array, load_img
import matplotlib.pyplot as plt
import numpy as np

def get_session_growth():
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth=True
    sess = tf.compat.v1.Session(config=config)
    return sess

sess = get_session_growth()

class Model:
    def __init__(self, image_size=(150,150)):
        self._height = image_size[0]
        self._width = image_size[1]

    def create_vgg_model(self):
        #  Load trained VGG16 weights
        vgg_model = VGG16(weights = 'imagenet', include_top = False, input_shape = (self._height, self._width, 3))
        #  Freeze the already trained layers
        for layer in vgg_model.layers:
            layer.trainable = False
        #  Extend the model to classify in two categories (busy/free)
        x = vgg_model.output
        x = Flatten()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        classifier_output = Dense(2, activation='sigmoid')(x)

        self._model = Model(inputs = vgg_model.input, outputs = classifier_output)
        self._model.compile(loss='binary_crossentropy',
              optimizer=SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

    def train(self, train_path, validate_path, number_train_samples = 4000, number_validation_samples = 500, batch_size = 8, epochs = 10):
        train_datagen =  ImageDataGenerator(preprocessing_function=preprocess_input,
            rotation_range=90,
            horizontal_flip=True,
            vertical_flip=True
            )
        train_generator = train_datagen.flow_from_directory(
            train_path, 
            target_size = (self._height, self._width),
            batch_size = batch_size,
            class_mode = 'binary')

        valid_datagen = ImageDataGenerator(rescale=1./255)
        validation_generator = valid_datagen.flow_from_directory(
            validate_path,
            target_size=(self._height, self._width),
            batch_size=batch_size,
            class_mode='binary')

        self._model.fit_generator(
        train_generator,
        steps_per_epoch=number_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=number_validation_samples // batch_size)

    def load_model_with_weights(self, json_path, weights_path):
        with open(json_path, 'r') as json_file:
            json_file_content = json_file.read()
            self._model = model_from_json(json_file_content)
        self._model.load_weights(weights_path)

    def save_model_with_weights(self, json_filename, weights_filename):
        with open(json_filename, "w") as json_file:
            json_file.write(self._model.to_json())
        self._model.save_weights(weights_filename)

    def load_model(self, path):
        self._model = load_model(path)

    def save_model(self, path):
        tf.keras.save_model(self._model, path)

    def predict(self, image):
        if self._model is None:
            raise Exception('Model is None')

        image_array = cv2.resize(image, (self._height, self._width)).astype(np.float32)
        image_array = np.expand_dims(image_array, axis = 0)
        return self._model.predict(image_array)
