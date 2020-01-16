import PIL
from PIL import Image, ImageTk
import cv2
from tkinter import *
import datetime
import os
from keras.models import load_model
import numpy as np

import pickle
from utils import get_landmarks

width, height = 600, 420
inWidth, inHeight = 100, 100

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

root = Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
lmain.pack()

index = 0
dateStart = datetime.datetime.now()

# load NN

model_lm = load_model("face_emotion_7_lm.h5")
mm_scalar = pickle.load(open("scalar_transform_lm", "rb"))

labels = ["angry", "fearful", "happy", "neutral", "sad", "surprise", "disgust"]
emotions = ["angry", "sad", "happy", "surprise", "disgust", "fearful", "neutral"]

last_em = ""



def getFace2(frame):
    img_height = len(frame)
    img_width = len(frame[0])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if(len(faces) > 0):
        x, y, w, h = faces[0]
        if(w >= img_width / 2 and h >= img_height / 2):
          return  cv2.resize(frame[y:y+h,x:x+w], (inWidth, inHeight))
    return []

def getFace(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    if(len(faces) > 0):
        x, y, w, h = faces[0]
        y -= 10
        x -= 10
        h += 20
        w += 20
        return cv2.resize(frame[y:y+h,x:x+w], (inWidth, inHeight))
    else:
        return None
    return cv2.resize(frame, (inWidth, inHeight))


def saveImage(image, emotion):
    date = datetime.datetime.now()
    day = date.strftime("%x")
    time = date.strftime("%X")

    if not os.path.exists(dateStart.strftime("%Y")+dateStart.strftime("%B")+dateStart.strftime("%d")+".csv"):
        f = open(dateStart.strftime("%Y")+dateStart.strftime("%B")+dateStart.strftime("%d")+".csv","w+")
        f.close()

    f = open(dateStart.strftime("%Y")+dateStart.strftime("%B")+dateStart.strftime("%d")+".csv", "a")
    f.write(f"{day};{time};{emotion}\n")
    f.close()


def classify_img_LM(img,lm, showSecond = False, showProb = False):
    global last_em
    # remove alpha if exists
    imar = np.array(img)[:, :, :3]
    lm = get_landmarks(imar)
    # print(lm)
    if isinstance(lm, type("")):
        # print("error finding landmarks")
        return
    lm = mm_scalar.transform([lm])
    pred = model_lm.predict(lm)[0].tolist()
    m2,p = 0,0
    for i in range(len(pred)):
        if m2 < pred[i] < max(pred):
            m2 = pred[i]
            p = i

    em = str(emotions[pred.index(max(pred))])
    if showProb:
        em += f"({int(max(pred)*100)}%)"
    if showSecond:
        em += f" {emotions[p]}"
        if showProb:
            em += f"({int(m2*100)}%)"

    if em != last_em:
        last_em = em
        return em
    else:
        return None


def show_frame(filename=None, name=None, save=False, show=True, showSecond = False, showProb = False):
    global index
    global last_em
    index += 1

    def call():
        show_frame(filename=filename, name=name,save=save,show=show,showSecond=showSecond ,showProb=showProb)

    ref, frame = cap.read()
    if ref:
        frame = cv2.flip(frame, 1)
        # frame = getFace(frame)

        if frame is None:
            pass
            # print("DICKS"+ str(index))
        else:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)

            em = classify_img_LM(img, last_em, showSecond=showSecond, showProb=showProb)
            # get emotion (is None if is the same)
            if em is not None:
                if show:
                    print(em)
                if save:
                    saveImage(frame, em + str(index))
    else:
        if not save:
            print("NO_FACE " + str(index))
    lmain.after(10, call)


def start(name,showSecond=False, showProb=False, save=True, show=True):
    show_frame(name=name, save=save, show=show, showSecond=showSecond, showProb= showProb)
    root.mainloop()

