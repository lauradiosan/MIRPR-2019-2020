import sqlite3

import cv2
from tensorflow.keras.models import load_model
from backend.db_access import DbAccess
import numpy as np


class ANNController:
    __MODEL_PATH = './models/model.h5'
    __HAARCASCADE_PATH = './haar_cascade/haarcascade_frontalface_default.xml'
    __FRAME_RATE = 0.2  # 5FPS
    __videoPath = ""
    __name = ""
    __start = ""
    __id = ""

    def __init__(self, db_access: DbAccess):

        self.db_access = db_access
        self.model = load_model(self.__MODEL_PATH)

    def set_session_id(self, session_id):

        if self.__id != "":
            return False
        self.__id = session_id
        return True

    def set_video_path(self, path):
        if self.__videoPath != "":
            return False
        self.__videoPath = path
        return True

    def set_start(self, start):
        if self.__start != "":
            return False
        self.__start = start
        return True

    def set_name(self, name):
        if self.__name != "":
            return False
        self.__name = name
        return True

    @staticmethod
    def __get_mean_probabilities_from_predictions(predictions):
        total_number_of_predictions = 0
        mean_probabilities = [0.0] * 7
        for pred in predictions:
            if pred is not None:
                total_number_of_predictions += 1
                current_probabilities = pred[0]
                for i in range(0, len(current_probabilities)):
                    mean_probabilities[i] += current_probabilities[i]
        if total_number_of_predictions > 0:
            for i in range(7):
                mean_probabilities[i] /= total_number_of_predictions
        return mean_probabilities

    @staticmethod
    def __get_dominant_emotion_from_predictions(mean_probabilities):
        dominant_emotion = -1
        max_value = 0
        for i in range(7):
            if max_value < mean_probabilities[i]:
                max_value = mean_probabilities[i]
                dominant_emotion = i
        return dominant_emotion

    def __process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(self.__HAARCASCADE_PATH)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
            prediction = self.model.predict(cropped_img.astype(np.float16))
            return prediction

    @staticmethod
    def __get_frame(cap, sec):
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        return cap.read()

    def predict_values(self):
        if self.__videoPath == "" or self.__start == "" or self.__name == "" or self.__id == "":
            return False
        cap = cv2.VideoCapture(self.__videoPath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = 1
        current_video_time_stamp = 0
        last_processed_frame_time_stamp = 0.0
        photo = None
        video_ended = False
        while not video_ended:
            predicted_emotions = []
            processed_frames = 0
            while processed_frames < 5 and not video_ended:
                ret, frame = cap.read()
                if ret:
                    frame_number = frame_number + 1
                    current_video_time_stamp = round(frame_number / fps, 1)
                    if current_video_time_stamp != last_processed_frame_time_stamp and \
                            current_video_time_stamp * 10 % 2 == 0:
                        predicted_emotions.append(self.__process_frame(frame))
                        processed_frames = processed_frames + 1
                        last_processed_frame_time_stamp = current_video_time_stamp
                        if current_video_time_stamp * 10 % 3 == 0:
                            # TODO: convert image to binary (sqlite blob) and save it in 'photo' variable
                            success, photo = cv2.imencode('.png', frame)
                            if success:
                                photo = sqlite3.Binary(photo)
                            else:
                                photo = None
                else:
                    video_ended = True
            mean_probabilities = self.__get_mean_probabilities_from_predictions(predicted_emotions)
            dominant_emotion = self.__get_dominant_emotion_from_predictions(mean_probabilities)

            self.db_access.add_session_details(
                session_id=self.__id,
                photo=photo,
                dominant_emotion=int(round(dominant_emotion)),
                video_time_stamp=current_video_time_stamp,
                prediction=mean_probabilities
            )
        self.__videoPath = ""
        self.__start = ""
        self.__name = ""
        self.__id = ""
        return True
