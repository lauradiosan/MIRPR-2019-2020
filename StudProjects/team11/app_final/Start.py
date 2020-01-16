from Login import face_from_webcam
from Aplicatie import start

login = False


if __name__ == '__main__':
    name = None
    if login:
        name = face_from_webcam()
    start(name, showSecond=True, showProb=False, save=True)
