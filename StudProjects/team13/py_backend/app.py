import os
import random
import string

from flask import Flask, request, jsonify
from flask_cors import CORS

from emotions.emotion import EmotionDetector
from login import recognise

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER_LOGIN'] = './static/unknown'
app.config['UPLOAD_FOLDER_EMOTION'] = './static/emotions'

emotion_detector = EmotionDetector()


def generateFilename():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))


@app.route("/", methods=['GET'])
def hello():
    return "HELLO"


@app.route("/login", methods=['POST'])
def login():
    f = request.files['image']
    filename = generateFilename() + ".png"
    filename = os.path.join(app.config['UPLOAD_FOLDER_LOGIN'], filename)
    f.save(filename)

    name = recognise(filename)
    response = {'name': name}
    # os.remove(filename)
    return jsonify(response)


@app.route("/emotion", methods=["POST"])
def getEmotion():
    f = request.files['emotion_image']
    filename = generateFilename() + ".png"
    filename = os.path.join(app.config['UPLOAD_FOLDER_EMOTION'], filename)
    f.save(filename)

    primary_emotion, secondary_emotion = emotion_detector.detectEmotion(filename)
    response = {'primary_emotion': primary_emotion, 'secondary_emotion': secondary_emotion}
    os.remove(filename)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
