import sys, os
import pandas as pd
import numpy as np
import cv2
import re
import shutil

PATH = "data"

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        img = cv2.imread(fullpath, 0)
        img = cv2.equalizeHist(img)

        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        idx = 0
        for (x, y, w, h) in faces:
            idx += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 1)
            roi_gray = img[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (200, 200))
            newpath = fullpath.split("\\")
            newpath[-3] = "data2"
            newpath = "\\".join(newpath)
            newpath = newpath[0:-4] + str(idx) + newpath[-4:]
            cv2.imwrite(newpath, roi_gray)