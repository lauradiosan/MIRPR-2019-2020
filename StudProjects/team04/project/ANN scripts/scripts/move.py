import re
import os
import shutil
import cv2

PATH = "data2-hist"

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
        newpath = fullpath
        newpath = newpath[:-4] + "k" + newpath[-4:]
        newpath = newpath.split("\\")
        newpath[0] = "data"
        newpath = "\\".join(newpath)
        # print(newpath)
        shutil.copy(fullpath, newpath)

        