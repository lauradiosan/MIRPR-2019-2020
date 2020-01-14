import os, shutil, cv2, numpy as np
from tensorflow.keras.models import load_model

PATH = 'jaffe'
MODELPATH = './model/model_fer.h5'

#model - 81% (antrenat pe FER + CAFE + CK+, validat pe CAFE + CK+)
#model_fer - 50% (validat pe CAFE + CK+)
#3model - 76% (antrenat pe FER + CAFE + CK+, validat pe CAFE + CK+)

model = load_model(MODELPATH)

predicted = 0
in_total = 0

di = {}
di = {0:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 1:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 
2:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 3:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 
4:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 5:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 
6:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}, 7:{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}}

emotions_fer = {0: 6, 1: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5}
emotions_fer_jaffe = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}

for path, dirs, files in os.walk(PATH):
    for filename in files:
        fullpath = os.path.join(path, filename)
        # print(path[-1])

        frame = cv2.imread(fullpath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            in_total += 1
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
            prediction = model.predict(cropped_img.astype(np.float16))
            pred = int(np.argmax(prediction))

            di[int(path[-1])][pred] += 1

            # if int(path[-1]) > 2:
            #     if pred == int(path[-1]) - 1:
            #         predicted += 1
            # else:
            #     if pred == int(path[-1]):
            #         predicted += 1
            if pred == emotions_fer_jaffe[int(path[-1])]:
                predicted += 1
                # print("OK")
            # else:
                # print("NOT OK")
            # cv2.putText(frame, emotion_dict[int(np.argmax(prediction))], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
print("Accuracy: " + str(predicted / in_total))
for k, v in di.items():
    print(k, v)