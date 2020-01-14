import json
from backend.configs import Configs
from backend.object_factory import ObjectFactory
from greenlet import greenlet
from flask_cors import cross_origin
from flask import request, send_file
import os
import io
app = ObjectFactory.app()
ANN_controller = ObjectFactory.ann_controller()
rest_controller = ObjectFactory.rest_controller()
socket_io = ObjectFactory.socket_io()
socket_controller = ObjectFactory.socket_controller()
VIDEO_PATH = os.getenv('APPDATA') + "temporary_file.mp4"
thread_pool = []
from PIL import Image

@app.route('/session', methods=['POST'])
@cross_origin()
def get_sessions():
    return rest_controller.get_sessions_handler()


@app.route('/session_details_emotions/<session_id>', methods=['POST'])
@cross_origin()
def get_session_details_emotions(session_id):
    return rest_controller.get_session_details_emotions_handler(session_id)


@app.route('/get_image_for_session_and_second/<session_id>/<video_time_stamp>', methods=['GET'])
@cross_origin()
def get_image_for_session_and_second(session_id, video_time_stamp):
    photo = rest_controller.get_image_for_session_and_second(session_id, video_time_stamp)
    # TODO: uncomment return after fixing bug
    if photo == None:
        return None
    picture_stream = io.BytesIO(photo)
    return send_file(
                     picture_stream,
                     attachment_filename='photo',
                     mimetype='image/png'
               )


@app.route('/start_session', methods=['POST'])
@cross_origin()
def start_session():
    session = socket_controller.start_session_handler()
    print('Session started.')
    return json.dumps({'id': session.id, 'start_time_stamp': session.start_time_stamp,
                       'end_time_stamp': session.end_time_stamp})


@app.route('/stop_session', methods=['POST'])
@cross_origin()
def stop_session():
    session = socket_controller.stop_session_handler()
    print('Session stopped.')
    return json.dumps({'id': session.id, 'start_time_stamp': session.start_time_stamp,
                       'end_time_stamp': session.end_time_stamp})


@app.route('/create_session', methods=['POST'])
@cross_origin()
def create_session():
    data = request.get_json() or request.form
    start = data.get('start')
    name = data.get('name')
    db_access = ObjectFactory.db_access()
    session = db_access.add_full_session(start, name)
    return json.dumps({'id': session.id, 'name': session.name, 'upload_time_stamp': session.upload_time_stamp})
@app.route('/process_video', methods=['POST'])
@cross_origin()
def process_video():
    video = request.files['video']
    video.save(VIDEO_PATH)
    data = request.get_json() or request.form
    start = data.get('start')
    name = data.get('name')
    id = data.get('id')
    db_access = ObjectFactory.db_access()
    session = db_access.get_session(id)
    if not (ANN_controller.set_session_id(session.id) and
            ANN_controller.set_start(start) and
            ANN_controller.set_name(name)
            and ANN_controller.set_video_path(VIDEO_PATH)):
        os.remove(VIDEO_PATH)
        return "Videoclipul ", 500
    if not ANN_controller.predict_values():
        os.remove(VIDEO_PATH)
        return "Values not set.", 500
    os.remove(VIDEO_PATH)
    return json.dumps({'id': session.id, 'name': session.name, 'upload_time_stamp': session.upload_time_stamp})

@socket_io.on('add_new_entry')
def handle_message(data):
    """

    :param data: contains photo on [0], screen_shot on [1], session_id on [2]
    session_id: the id of the current session
    screen_shot: a screen shot from a user
    photo: a photo from the users's webcam
    :return:
    """
    photo = data[0]
    screen_shot = data[1]
    session_id = data[2]
    g = greenlet(socket_controller.message_handler)
    g.switch(photo, screen_shot, session_id)


@socket_io.on('connect')
def handle_connect():
    print('Client connected')


@socket_io.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    app.run(threaded = True, host=Configs.server_ip, port=Configs.port)
