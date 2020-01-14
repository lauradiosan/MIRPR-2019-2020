import re
import os
import shutil
import cv2

PATH = "data"

emotions = [
    "neutral",
    "angry",
    "contempt",
    "disgust", 
    "fear", 
    "happy", 
    "sad", 
    "surprise"
]

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        img = cv2.imread(fullpath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(fullpath, gray)