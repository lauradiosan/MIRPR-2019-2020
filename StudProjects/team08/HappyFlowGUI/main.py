import copy
import os
import time
import tensorflow as tf

import numpy as np
from absl import app, flags, logging
from absl.flags import FLAGS
from tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk


import tkinter.filedialog

from yolov3_tf2.dataset import transform_images
from yolov3_tf2.models import YoloV3
from yolov3_tf2.utils import draw_outputs

flags.DEFINE_string('classes', './data/person.names', 'path to classes file')
flags.DEFINE_string('weights', './weights/yolov3_train_48.tf', 'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_integer('num_classes', 1, 'number of classes in the model')
flags.DEFINE_string('video_output', 'test.avi', 'path to output video')
flags.DEFINE_string('video_output_format', 'XVID', 'codec used in VideoWriter when saving video to file')


class Controller:

    def __init__(self):
        self.__yolo = None
        self.__class_names = None

        self.initialize_yolo()

    def initialize_yolo(self):
        self.__yolo = YoloV3(classes=FLAGS.num_classes)
        self.__yolo.load_weights(FLAGS.weights).expect_partial()
        logging.info('weights loaded')

        self.__class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
        logging.info('classes loaded')

    def detect_image(self, image_path):
        logging.info('image path: ' + image_path)

        # open raw image
        img_raw = tf.image.decode_image(
            open(image_path, 'rb').read(), channels=3)
        # attach a new dimension to make it a tensor
        img = tf.expand_dims(img_raw, 0)

        # resize the image to the default dimension for network: 416 x 416 and to 0-1 rgb spectrum
        img = transform_images(img, FLAGS.size)

        # obtain results
        boxes, scores, classes, nums = self.__yolo(img)

        # compute output image with cv2 and return it
        img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
        img = draw_outputs(img, (boxes, scores, classes, nums), self.__class_names)
        return img

    def detect_from_camera(self, save_video=False):

        # use cv2 to get reference to our video camera
        video_capture = cv2.VideoCapture(0)

        # small initialization
        times = []
        output_stream = None

        # if we also want to save the video
        if FLAGS.video_output and save_video:
            # by default VideoCapture returns float instead of int
            width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
            output_stream = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))

        while True:
            _, img = video_capture.read()

            if img is None:
                logging.warning("Empty Frame")
                time.sleep(0.1)
                continue

            img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_in = tf.expand_dims(img_in, 0)
            img_in = transform_images(img_in, FLAGS.size)

            t1 = time.time()
            boxes, scores, classes, nums = self.__yolo.predict(img_in)
            t2 = time.time()
            times.append(t2 - t1)
            times = times[-20:]

            img = draw_outputs(img, (boxes, scores, classes, nums), self.__class_names)
            img = cv2.putText(img, "Time: {:.2f}ms".format(sum(times) / len(times) * 1000), (0, 30),
                              cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
            if FLAGS.video_output and save_video:
                output_stream.write(img)
            cv2.imshow('output', img)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()


class UILayout:

    def __init__(self, master_root, controller):
        self.__toolbar = None
        self.__select_button = None
        self.__process_button = None
        self.__live_camera_button = None
        self.__status_bar = None
        self.__input_image_panel = None
        self.__output_image_panel = None
        self.__middle_frame = None
        self.__current_input_image_path = None
        self.__status_bar_message = StringVar()

        self.__main_frame = Frame(master_root)
        self.__main_frame.pack(fill=BOTH, expand=TRUE)
        self.__controller = controller
        self.compute_layout()

    def compute_layout(self):

        self.compute_toolbar()
        self.compute_image_panels()
        self.compute_status_bar()

    def compute_toolbar(self):
        self.__toolbar = Frame(self.__main_frame)

        self.__select_button = Button(self.__toolbar, text="Select an image", command=self.select_image)
        self.__select_button.pack(side=LEFT, padx="5", pady="5")

        self.__process_button = Button(self.__toolbar, text="Process image", command=self.process_image)
        self.__process_button.pack(side=LEFT, padx="5", pady="5")
        self.__process_button['state'] = 'disabled'

        self.__live_camera_button = Button(self.__toolbar, text='Open camera', command=self.open_camera)
        self.__live_camera_button.pack(side=LEFT, padx="5", pady="5")

        self.__toolbar.pack(side=TOP)

    def compute_image_panels(self):
        self.__middle_frame = Frame(self.__main_frame)
        self.__middle_frame.pack()

        # take no image selected for default version
        no_image_selected = PhotoImage(file="photos/no_image_selected.png")

        self.__input_image_panel = Label(self.__middle_frame, image=no_image_selected)
        self.__input_image_panel.image = no_image_selected
        self.__input_image_panel.pack(side=LEFT, padx=10, pady=10)

        self.__output_image_panel = Label(self.__middle_frame, image=no_image_selected)
        self.__output_image_panel.image = no_image_selected
        self.__output_image_panel.pack(side=RIGHT, padx=10, pady=10)

    def compute_status_bar(self):
        # Status Bar for printing our current state
        self.__status_bar_message.set('Ready to work')
        self.__status_bar = Label(self.__main_frame, textvariable=self.__status_bar_message, bd=1, relief=SUNKEN, anchor=W)
        self.__status_bar.pack(side=BOTTOM, fill=X)

    def select_image(self):
        image_path = tkinter.filedialog.askopenfilename()

        if len(image_path) > 0:
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            resized = image.resize((640, 480), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(resized)

            self.__input_image_panel.configure(image=image)
            self.__input_image_panel.image = image
            self.__process_button['state'] = 'normal'
            self.__current_input_image_path = image_path

    def process_image(self):
        # button becomes disabled and we change the status bar
        self.__process_button['state'] = 'disabled'

        # change status bar to working
        self.__status_bar_message.set('Processing in progress')

        # detection
        output_image = self.__controller.detect_image(self.__current_input_image_path)

        # process image to make sure it works with tkinter ..
        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        output_image = Image.fromarray(output_image)
        resized = output_image.resize((640, 480), Image.ANTIALIAS)
        output_image = ImageTk.PhotoImage(resized)

        # assign the output image to our layout
        self.__output_image_panel.configure(image=output_image)
        self.__output_image_panel.image = output_image

        #  invalidate path (not allowing to overload the ui) and reset status bar
        self.__current_input_image_path = ''
        self.__status_bar_message.set('Ready to work')

    def open_camera(self):
        self.__controller.detect_from_camera()


def main(_argv):
    controller = Controller()
    root = Tk()
    ui_layout = UILayout(root, controller)

    root.mainloop()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
