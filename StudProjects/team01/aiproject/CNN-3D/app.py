import os

from flask_cors import cross_origin
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import base64
from train import *
from flask import send_file
from convert import write_gif_normal  # convert_nifti_to_gif

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'nii'}

UPLOAD_FOLDER = './files'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process-image', methods=["POST"])
@cross_origin()
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
        with open(write_gif_normal(os.path.join(app.config['UPLOAD_FOLDER'], filename)), mode='rb') as f:
            img = f.read()
        response_dict = {'file': base64.encodebytes(img).decode('utf-8')}
        s = get_prediction(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response_dict['message'] = 'You are right' if request.form['malformation'] == s \
            else 'Unfortunately, you missed this'
        resp = jsonify(response_dict)
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are nii'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(host='172.30.118.59')
