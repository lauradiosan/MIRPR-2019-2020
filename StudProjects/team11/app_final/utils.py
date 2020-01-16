import numpy as np
import math
import cv2
import dlib


clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def get_landmarks(image, show=False):
    resized = cv2.resize(image, (350, 350))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    clahe_img = clahe.apply(gray)

    detections = detector(clahe_img, 1)
    if len(detections) < 1:
        return "error"

    for k, d in enumerate(detections):
        shape = predictor(clahe_img, d)
        xlist = []
        ylist = []
        for i in range(1, 68):
            xlist.append(float(shape.part(i).x))
            ylist.append(float(shape.part(i).y))

        xmean = np.mean(xlist)
        ymean = np.mean(ylist)

        xcentral = [(x - xmean) for x in xlist]
        ycentral = [(y - ymean) for y in ylist]

        if show:
            for i in range(67):
                cv2.circle(clahe_img, (int(xlist[i]), int(ylist[i])), 1, (0, 0, 255), thickness=2)
                cv2.circle(clahe_img, (int(xmean), int(ymean)), 1, (255, 0, 0), thickness=2)

            cv2.imshow(clahe_img)

        landmarks_vectorised = []
        for x, y, w, z in zip(xlist, ylist, xcentral, ycentral):
            meannp = np.asarray((ymean, xmean))
            coornp = np.asarray((z, w))
            dist = np.linalg.norm(coornp - meannp)
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append((math.atan2(y, x) * 360) / (2 * math.pi))
    return landmarks_vectorised
