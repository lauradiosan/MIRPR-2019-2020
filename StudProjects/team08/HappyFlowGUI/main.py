from tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk

import tkinter.filedialog

panelA = None
panelB = None
processBtn = None
imagePath = ''

def get_processed_image(option):
    image = 'photos/' + option + '.jpg'
    processed_image = 'photos/' + option + 'Processed.jpg'

    img = cv2.imread(image)
    cv2.imshow('image', img)

    processed_img = cv2.imread(processed_image)
    cv2.imshow('processed image', processed_img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def select_image():
    global panelA
    global processBtn
    global imagePath

    path = tkinter.filedialog.askopenfilename()

    if len(path) > 0:
        imagePath = path

        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if panelA is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            processBtn['state'] = 'normal'
        else:
            panelA.configure(image = image)
            panelA.image = image
            processBtn['state'] = 'normal'


def process_image():

    global processBtn
    global panelB
    global imagePath

    processedImagePath = imagePath[:-4] + 'Processed.jpg'

    processedImage = cv2.imread(processedImagePath)
    processedImage = cv2.cvtColor(processedImage, cv2.COLOR_BGR2RGB)
    processedImage = Image.fromarray(processedImage)
    processedImage = ImageTk.PhotoImage(processedImage)

    if panelB is None:
        panelB = Label(image=processedImage)
        panelB.image = processedImage
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelB.configure(image = processedImage)
        panelB.image = processedImage

    processBtn['state'] = 'disabled'


def main():
    global processBtn

    root = Tk()

    btn = Button(root, text="Select an image", command=select_image)
    btn.pack(side="top", fill="both", expand="yes", padx="10", pady="10")

    processBtn = Button(root, text="Process image", command=process_image)
    processBtn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    processBtn['state'] = 'disabled'


    root.mainloop()

'''
    print("Which image would you like to process?")
    print("1, 2 or 3?")
    option = str(input())
    get_processed_image(option)
'''

if __name__ == "__main__":
    main()
