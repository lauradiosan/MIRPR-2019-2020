import os
import face_recognition
import cv2
from Aplicatie import cap

def load_face(face):
    current_face = cv2.imread('%s/%s' % (known_faces_dir, face))
    return face_recognition.face_encodings(current_face)[0]


def face_from_webcam():
    webcam = cap#cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haar_cascade.xml')

    while True:
        _, img = webcam.read()

        height, width, _ = img.shape

        x1, y1, x2, y2 = (int(width*(3/8)), int(height/4), int(width*(5/8)), int(height*(3/4)))

        img_center = img[y1:y2, x1:x2]
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0))

        detected_faces = face_cascade.detectMultiScale(img_center)

        if len(detected_faces) != 0:
            (x, y, w, h) = detected_faces[0]
            face = img_center[y: y+h, x:x+w]
            user_name = match_known_face(face)
            if user_name:
                cv2.destroyWindow("Login")
                return user_name

        cv2.imshow('Login', img)
        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyAllWindows()
            break


def match_known_face(inp):
    known_faces_dir = 'known_faces'
    faces = os.listdir(known_faces_dir)


    encodings = face_recognition.face_encodings(inp)

    if len(encodings) == 0:
        return None

    res = face_recognition.compare_faces([load_face(face) for face in faces], encodings[0])

    print(res)

    recognised = res.index(True)
    if recognised == -1:
        return None

    return faces[recognised]

