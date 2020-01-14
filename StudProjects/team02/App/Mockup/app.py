from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
from controller.repository import Repository
from controller.classify import predict
from controller.frame_capture import YoutubeVideoWrapper
from controller.utils import increase_contrast
from tinydb import TinyDB, Query
import time
from werkzeug.utils import secure_filename
import os
import json
import threading
import cv2
from PIL import Image

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


start_time = None
configuration = None
yt_video_wrapper = None


def update_prediction():
    while True:
        frame_time = int(time.time() - start_time)
        yt_video_wrapper.set_seconds(frame_time)
        image = yt_video_wrapper.get_current_image()
        image = increase_contrast(image)
        cv2.imwrite('frame.png', image)
        pil_image = Image.open('frame.png')
        predict('./controller/db.json', pil_image)
        print("updated ", frame_time)
        time.sleep(configuration.get('timer'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/spots', methods=['GET'])
def get_spots():
    spots = repo.get_all()
    # time.sleep(5)
    return jsonify(spots)


@app.route('/upload', methods=['POST'])
def upload_frame():
    if request.files['file']:
        frame = request.files['file']
        filename = secure_filename(frame.filename)
        destination = os.path.join('./frames', filename)
        print(destination)
        frame.save(destination)
        return "success"


@app.route('/status', methods=['GET'])
def get_status():
    response = {}
    response['spots'] = TinyDB('./controller/db.json').all()
    response['elapsed'] = time.time() - start_time
    response['next_prediction'] = 8
    return jsonify(response)


if __name__ == '__main__':
    start_time = time.time()           
    with open('configuration.json', 'r') as file:
        configuration = json.load(file)
    yt_video_wrapper = YoutubeVideoWrapper(configuration.get('url'))
    update_thread = threading.Thread(target=update_prediction)
    update_thread.start()
    app.run(host= '0.0.0.0', port=5000)