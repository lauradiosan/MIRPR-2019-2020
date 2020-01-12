import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from train import *
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'nii'}

UPLOAD_FOLDER = './files'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process-image', methods=["POST"])
def process_image():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        s = get_prediction(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message': s})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are nii'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run()
