import socketio
from user_client.configs import Configs
import threading
import mss
import mss.tools
from time import sleep
import cv2
from socketio.exceptions import ConnectionError


class SendData(threading.Thread):

    def __init__(self, socket: socketio.Client, session_id, *args, **kwargs):
        super(SendData, self).__init__(*args, **kwargs)
        self._stopper = threading.Event()
        self.socket = socket
        self.session_id = session_id

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            video_capture = cv2.VideoCapture(0)
            if not video_capture.isOpened():
                raise Exception("Could not open video device")
            with mss.mss() as sct:
                for i in range(4):
                    monitor = sct.monitors[1]
                    im = sct.grab(monitor)
                    screen_shot_raw_bytes = mss.tools.to_png(im.rgb, im.size)
                    successful, web_cam_photo_raw_bytes = video_capture.read()
                    if not successful:
                        raise Exception("Photo not captured")
                    self.socket.emit('add_new_entry',
                                     [web_cam_photo_raw_bytes.tobytes(), screen_shot_raw_bytes, self.session_id])
                    sleep(1/5)  # sends 5 screenshots and 5 webcam photos every second to the backend
            video_capture.release()


HOST = Configs.host_ip
PORT = Configs.host_port
socketIO = socketio.Client()
while True:
    try:
        socketIO.connect(f"amqp://{HOST}:{PORT}")
        sending_thread = [SendData(socketIO, -1)]
        print('Connected to backend!')
        break
    except socketio.exceptions.ConnectionError:
        print('Not connected yet.')
        sleep(0.5)


@socketIO.on('session_started')
def session_started(session_id):
    print('Session started.')
    sending_thread[0] = SendData(socketIO, session_id)
    sending_thread[0].start()
    sending_thread[0].join()


@socketIO.on('session_stopped')
def session_stopped(data):
    print('Session stopped.')
    sending_thread[0].stop()
