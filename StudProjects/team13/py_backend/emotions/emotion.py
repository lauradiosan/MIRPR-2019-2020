import cv2
import numpy as np
import tensorflow as tf
from keras_preprocessing.image import img_to_array

PATH_TO_HAAR = "C:\\Users\\raduc\\Desktop\\ai\\git\\emotionkids\\login_app_server\\res\\haar.xml"


class EmotionDetector:
    def __init__(self):
        # self.model = load_model("./res/emotions_model.hdf5")
        self.model = tf.keras.models.load_model("./res/fer/trained_model_resnet_improving.hdf5")
        emotion_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
        self.labels = dict((k, v) for k, v in emotion_dict.items())

    @staticmethod
    def face_detector(img):
        face_classifier = cv2.CascadeClassifier(PATH_TO_HAAR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]

        try:
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        except:
            return (x, w, y, h), np.zeros((48, 48), np.uint8), img
        return (x, w, y, h), roi_gray, img

    def detectEmotion(self, filename):
        face_image = cv2.imread(filename)
        rect, face, image = self.face_detector(face_image)
        if np.sum([face]) != 0.0:
            roi = face.astype("float") / 255.0  # region of interest
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # make a prediction on the ROI, then lookup the class
            preds = self.model.predict(roi)[0]
            label = self.labels[preds.argmax()]
            second_best = np.array([preds[x] for x in range(len(preds)) if x != preds.argmax()]).argmax()
            try:
                second_best = second_best[0]
            except IndexError:
                pass
            label2 = self.labels[second_best]
            return label, label2
        else:
            return "No face detected", ""
