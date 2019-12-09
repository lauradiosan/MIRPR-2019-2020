import json
import numpy as np
from flask import render_template, request, Response
import cv2
from app import app
from app.camera import VideoCamera
from app.model_train.predict import *

"""
global image_num
image_num = 0

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_chunk', methods=['GET', 'POST'])
def process_chunk():
    global image_num
    img = np.zeros((320, 480, 3), dtype=np.uint8)
    blob = request.form['image']
    blob = json.loads(blob)
    print(len(blob))
    cnt = 0
    for i in range(0, len(blob), 4):
        curr = str(i)
        curr_1 = str(i + 1)
        curr_2 = str(i + 2)
        r = blob[curr]
        g = blob[curr_1]
        b = blob[curr_2]
        # print("B: " + str(b) + " G: " + str(g) + " R: " + str(r))
        row = cnt // 480
        col = cnt % 480
        cnt += 1
        img[row][col][0] = b
        img[row][col][1] = g
        img[row][col][2] = r
    #print(img)

    img = np.array(img, dtype=np.uint8)
    frame = img
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img, orig_im, dim = prep_image(frame, inp_dim)

    im_dim = torch.FloatTensor(dim).repeat(1, 2)

    im_dim = im_dim.cuda()
    img = img.cuda()

    output = model(Variable(img), CUDA)
    output = write_results(output, confidence, num_classes, nms=True, nms_conf=nms_thesh)

    output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(inp_dim)) / inp_dim

    im_dim = im_dim.repeat(output.size(0), 1)
    output[:, [1, 3]] *= frame.shape[1]
    output[:, [2, 4]] *= frame.shape[0]

    list(map(lambda x: write(x, orig_im), output))

    #print(orig_im.shape)
    image_num += 1
    img_path = r'C:\\Users\georg\Desktop\MIRPR\Proj-Faraday-WebApp\app\static\images\img' + str(image_num) + '.jpg'
    cv2.imwrite(img_path, orig_im)
    # img_dict = {}
    # cnt = 0
    # for i in range(len(orig_im)):
    #     for j in range(len(orig_im[0])):
    #         img_dict[str(cnt)] = [i, j, int(orig_im[i][j][0]), int(orig_im[i][j][1]), int(orig_im[i][j][2])]
    #         cnt += 1
    # return json.dumps(img_dict)
    return json.dumps({'image_url': 'http://127.0.0.1:5000/static/images/img' + str(image_num) + '.jpg'})
"""


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_unprocessed(camera):
    while True:
        frame = camera.get_frame_unprocessed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_1')
def video_feed_1():
    return Response(gen_unprocessed(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
