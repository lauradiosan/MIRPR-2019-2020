"""https://www.tensorflow.org/tutorials/images/classification"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import time

from io import BytesIO

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from skimage import io
from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                     MaxPooling2D)
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import image as tfImage
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

from PIL import Image as PILImage

from .image_type import ImageType
# from image_type import ImageType


class ImageClassifier:
    def __init__(self, saved_data_directory=None,model_id=None):
        self.__batch_size = 64
        self.__number_of_epochs = 10
        self.__image_height = 150
        self.__image_width = 150
        self.__number_of_classes = 3
        self.__learning_rate = 0.01

        self.__saved_data_directory = saved_data_directory
        # Used for identifying the model.
        self.__model_id = str(int(time.time())) if model_id is None else model_id

        self.__absolute_directory_path = os.path.dirname(os.path.abspath(__file__))
        self.__probability_threshold = 0.6


    def get_learning_rate(self):
        return self.__learning_rate


    def set_learning_rate(self, learning_rate):
        self.__learning_rate = learning_rate


    def build_image_classifier(self):
        if hasattr(self, '__model'):
            print("The model is already built.")
            return
        self.__set_image_directories()
        self.__set_input_data_size()
        self.__log_model_information()
        self.__build_data_generators()
        self.__create_model()
        self.__compile_model()
        self.__train_model()
        self.__plot_results()


    def save_model(self):
        """Saves the current model to self.__saved_data_directory."""
        filename = "image_classifier_model_%s.h5" % self.__model_id
        saved_model_file = os.path.join(self.__saved_data_directory, filename)
        self.__model.save(saved_model_file)


    def load_model(self):
        """Loads the model from a file from self.__saved_data_directory."""
        filename = "image_classifier_model_%s.h5" % self.__model_id
        saved_model_file = os.path.join(self.__saved_data_directory, filename)
        self.__model = tf.keras.models.load_model(saved_model_file)


    def classify(self, image_as_numpy_array):
        """Returns the type of the given image together with all the
        probabilities (self.__number_of_classes probabilities)."""
        prediction = self.__model.predict_classes(image_as_numpy_array, 	   
                                                  batch_size=self.__batch_size)
        print(prediction)

        probabilities = self.__model.predict(image_as_numpy_array,
                                             batch_size=self.__batch_size)
        print("probabilities = ", probabilities)
        probabilities = probabilities[0]
        print(probabilities)
        for index in range(len(probabilities)):
            if probabilities[index] >= self.__probability_threshold:
                return ImageType(index)
        return ImageType.OTHERS


    def image_as_numpy_array(self, filename):
        img = tfImage.load_img(filename, target_size=(self.__image_height, self.__image_width))
        img_as_array = np.array(img)
        return np.array([img_as_array])


    def image_bytes_as_numpy_array(self, image_bytes, widht, height):
        pil_image = PILImage.open(BytesIO(image_bytes))
        pil_image = pil_image.resize((self.__image_width, self.__image_height))
        img_as_array = np.array(pil_image)
        return np.array([img_as_array])
        

    def __set_image_directories(self):
        """Should be called only once."""
        self.__images_path = os.path.join(self.__absolute_directory_path, 'images/')
        self.__train_directory = os.path.join(self.__images_path, 'train')
        self.__validation_directory = os.path.join(self.__images_path, 'validation')

        self.__train_forest_directory = \
            os.path.join(self.__train_directory, 'forest')
        self.__train_sand_beach_directory = \
            os.path.join(self.__train_directory, 'sand_beach')
        self.__train_snow_mountain_directory = \
            os.path.join(self.__train_directory, 'snow_mountain')

        self.__validation_forest_directory = \
            os.path.join(self.__validation_directory, 'forest')
        self.__validation_sand_beach_directory = \
            os.path.join(self.__validation_directory, 'sand_beach')
        self.__validation_snow_mountain_directory = \
            os.path.join(self.__validation_directory, 'snow_mountain')


    def __set_input_data_size(self):
        """Should be called only once."""
        self.__train_forest_number = \
            len(os.listdir(self.__train_forest_directory))
        self.__train_sand_beach_number = \
            len(os.listdir(self.__train_sand_beach_directory))
        self.__train_snow_mountain_number = \
            len(os.listdir(self.__train_snow_mountain_directory))

        self.__validation_forest_number = \
            len(os.listdir(self.__validation_forest_directory))
        self.__validation_sand_beach_number = \
            len(os.listdir(self.__validation_sand_beach_directory))
        self.__validation_snow_mountain_number = \
            len(os.listdir(self.__validation_snow_mountain_directory))

        self.__total_train_size = self.__train_sand_beach_number \
            + self.__train_snow_mountain_number \
            + self.__train_forest_number
        self.__total_validation_size = self.__validation_sand_beach_number \
            + self.__validation_snow_mountain_number \
            + self.__validation_forest_number


    def __log_model_information(self):
        """Should be called only once."""
        # TODO: use logger
        print('Total training forest images:', \
            self.__train_forest_number)
        print('Total training sand beache images:', \
            self.__train_sand_beach_number)
        print('Total training snow mountain images:', \
            self.__train_snow_mountain_number)

        print('Total validation forest images:', \
            self.__validation_forest_number)
        print('Total validation sand beache images:', \
            self.__validation_sand_beach_number)
        print('Total validation snow mountain images:', \
            self.__validation_snow_mountain_number)

        print('Total training images:', self.__total_train_size)
        print('Total validation images:', self.__total_validation_size)


    def __build_data_generators(self):
        """Build image generators for training and validations.

        Our data will use a wide assortment of transformations to try and
        squeeze as much variety as possible out of our image corpus."""
        train_image_generator = \
             ImageDataGenerator(rescale=1./255,
                                horizontal_flip=True,
                                rotation_range=15,
                                width_shift_range=0.15,
                                height_shift_range=0.15,
                                shear_range=0.2,
                                zoom_range=0.5)
        validation_image_generator = \
            ImageDataGenerator(rescale=1./255,
                               horizontal_flip=True,
                               rotation_range=15,
                               width_shift_range=0.15,
                               height_shift_range=0.15,
                               shear_range=0.2,
                               zoom_range=0.5)

        self.__train_data_generator = train_image_generator.flow_from_directory(
            batch_size = self.__batch_size,
            directory = self.__train_directory,
            shuffle = True,
            target_size = (self.__image_height, self.__image_width),
            class_mode = 'categorical')
        self.__validation_data_generator = validation_image_generator.flow_from_directory(
            batch_size = self.__batch_size,
            directory = self.__validation_directory,
            target_size = (self.__image_height, self.__image_width),
            class_mode = 'categorical')


    def __create_model(self):
        self.__model = Sequential([
            Conv2D(16, 3, padding='same', activation='relu', input_shape=(self.__image_height, self.__image_width, 3)),
            MaxPooling2D(),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Dropout(0.2),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(self.__number_of_classes, activation='softmax')
        ])


    def __compile_model(self):
        self.__model.compile(optimizer=tf.keras.optimizers.Adam(lr=self.__learning_rate), 
                             loss='categorical_crossentropy',
                             metrics=['accuracy'])
        self.__model.summary()


    def __train_model(self):
        self.__history = self.__model.fit_generator(
            self.__train_data_generator,
            epochs=self.__number_of_epochs,
            steps_per_epoch=self.__total_train_size // self.__batch_size,
            validation_data=self.__validation_data_generator,
            validation_steps=self.__total_validation_size // self.__batch_size
        )


    def train_model(self):
        if not hasattr(self, '__train_data_generator') or \
           not hasattr(self, '__validation_data_generator'):
            self.__set_image_directories()
            self.__set_input_data_size()
            self.__build_data_generators()
        self.__history = self.__model.fit_generator(
            self.__train_data_generator,
            epochs=self.__number_of_epochs,
            steps_per_epoch=self.__total_train_size // self.__batch_size,
            validation_data=self.__validation_data_generator,
            validation_steps=self.__total_validation_size // self.__batch_size
        )
        self.__plot_results()


    def __plot_results(self):
        acc = self.__history.history['acc']
        val_acc = self.__history.history['val_acc']

        loss = self.__history.history['loss']
        val_loss = self.__history.history['val_loss']

        epochs_range = range(self.__number_of_epochs)

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')

        # Save the plot to a file.
        filename = "training_and_validation_%s.png" % self.__model_id
        plot_file = os.path.join(self.__saved_data_directory, filename)
        plt.savefig(plot_file)
        
        # Clear plot for future uses.
        plt.clf()


if __name__ == '__main__':
    ABSOLUTE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
        
    saved_data_directory = os.path.join(ABSOLUTE_DIRECTORY_PATH, 'saved_model')
    image_classifier = ImageClassifier(saved_data_directory=saved_data_directory,model_id='10')
    # image_classifier = ImageClassifier(saved_data_directory=saved_data_directory)
    # image_classifier.build_image_classifier()
    # image_classifier.save_model()
    image_classifier.load_model()

    image_path_1 = os.path.join(ABSOLUTE_DIRECTORY_PATH, 'images/validation/sand_beach/00000000.jpg')
    print(image_classifier.classify(image_classifier.image_as_numpy_array(image_path_1)))
    img = mpimg.imread(image_path_1)
    imgplot = plt.imshow(img)
    # plt.show()

    image_path_2 = os.path.join(ABSOLUTE_DIRECTORY_PATH, 'images/validation/snow_mountain/00000642.jpg')
    print(image_classifier.classify(image_classifier.image_as_numpy_array(image_path_2)))
    img = mpimg.imread(image_path_2)
    imgplot = plt.imshow(img)
    # plt.show()

    image_path_3 = os.path.join(ABSOLUTE_DIRECTORY_PATH, 'images/validation/forest/00000558.jpg')
    print(image_classifier.classify(image_classifier.image_as_numpy_array(image_path_3)))
    img = mpimg.imread(image_path_3)
    imgplot = plt.imshow(img)
    # plt.show()

    image_path_4 = os.path.join(ABSOLUTE_DIRECTORY_PATH, 'images/others/cactuses.jpg')
    print(image_classifier.classify(image_classifier.image_as_numpy_array(image_path_4)))
    img = mpimg.imread(image_path_4)
    imgplot = plt.imshow(img)
    # plt.show()
