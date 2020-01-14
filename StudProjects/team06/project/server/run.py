import logging

from datetime import timedelta

from flask import Flask, request, session, send_file
from flask_cors import CORS
# from flask.ext.session import Session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from analyzer.analyzer import Analyzer
from services.booking_service import BookingService
from services import booking_utils
from text_preprocessor.wordcloud_utils import create_wordcloud

import io
import os
import time
import uuid
import zipfile
import json

app = Flask(__name__)

app.config.from_object(__name__)
CORS(app)
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_FILE_THRESHOLD'] = 100

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hp_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)

db = SQLAlchemy(app)


class HolidayPlan(db.Model):
    id = db.Column(db.String(100), 
                   primary_key=True)
    analyzer_as_json = db.Column(db.JSON,
                                 index=False,
                                 unique=False)

    def __repr__(self):
        return '<HolidayPlan %s %s>' % (self.id, self.analyzer_as_json)    


@app.route('/reset', methods=['GET'])
def reset():
    if not 'holiday_plan_id' in request.cookies:
        return ''
    holiday_plan_id = request.cookies['holiday_plan_id']
    if holiday_plan_id and \
        HolidayPlan.query.filter_by(id=holiday_plan_id).scalar() is not None:
        HolidayPlan.query.filter_by(id=holiday_plan_id).delete()
        db.session.commit()
    return ''


@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    """TODO

    Returns vacation_requirements"""
    input_text = request.args.get('input_text')
    # print(request)
    # print(input_text)
    # print(session.sid)
    # print(session.keys())
    if not input_text:
        return ''

    holiday_plan_id = request.cookies['holiday_plan_id']
    analyzer = get_analyzer(holiday_plan_id)
    analyzer.analyse(input_text)
    vacation_requirements = analyzer.get_vacation_requirements()
    save_analyzer(holiday_plan_id, analyzer)

    # logging.basicConfig(format='%(asctime)-15s %(message)s')
    # logger = logging.getLogger('HolidayChatbot')

    # logger.info("=======Vacation Requirements=======")
    # logger.info("cities: %s", str(vacation_requirements.cities))
    # logger.info("start_date: %s", str(vacation_requirements.start_date))
    # logger.info("end_date: %s", str(vacation_requirements.end_date))
    # logger.info("number_of_rooms: %s", str(vacation_requirements.number_of_rooms))
    # logger.info("number_of_children: %s", str(vacation_requirements.number_of_children))
    
    print("=======Vacation Requirements=======")
    print("cities: %s", str(vacation_requirements.cities))
    print("start_date: %s", str(vacation_requirements.start_date))
    print("end_date: %s", str(vacation_requirements.end_date))
    print("number_of_rooms: %s", str(vacation_requirements.number_of_rooms))
    print("number_of_children: %s", str(vacation_requirements.number_of_children))

    return vacation_requirements.to_json()


@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    """TODO

    Returns vacation_requirements"""
    image_data = request.data
    width = request.args.get('width')
    height = request.args.get('height')
    if not image_data:
        print('Missing arguments.')
        return ''

    holiday_plan_id = request.cookies['holiday_plan_id']
    analyzer = get_analyzer(holiday_plan_id)
    analyzer.analyse_image(image_data, width, height)
    vacation_requirements = analyzer.get_vacation_requirements()
    save_analyzer(holiday_plan_id, analyzer)

    return vacation_requirements.to_json()


@app.route('/hotels-list', methods=['GET'])
def get_hotels_list():
    return {"result": [{
        "hotel_id": 1,
        "hotel_name": "Apex Temple Court Hotel",
        "sentiment": 0.83,
        "url": "https://www.booking.com/hotel/gb/apex-temple-court.en-gb.html"
    }]}

    # TODO: make this work again
    holiday_plan_id = request.cookies['holiday_plan_id']
    analyzer = get_analyzer(holiday_plan_id)
    vacation_requirements = analyzer.get_vacation_requirements()
    booking_service = BookingService()
    return booking_service.get_hotels_list(vacation_requirements)


@app.route('/hotel-reviews-wordcloud', methods=['GET'])
def get_hotel_reviews_wordcloud():
    # TODO: delete this
    negative_reviews_filename = "1_negative_reviews_wordcloud.png"
    positive_reviews_filename = "1_positive_reviews_wordcloud.png"
    
    filename_negative = 'datasets/hotel_reviews_booking/wordclouds/1_2_Serjeant_s_Inn_Fleet_Street_City_of_London_London_EC4Y_1LL_United_Kingdom__Negative_Review.png'
    filename_positive = 'datasets/hotel_reviews_booking/wordclouds/1_2_Serjeant_s_Inn_Fleet_Street_City_of_London_London_EC4Y_1LL_United_Kingdom__Positive_Review.png'
    # Sends the result as a zip file
    zip_name = '1_reviews.zip'
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        image_bytes = open(os.path.join(basedir, filename_negative), "rb").read()
        image_bytes = bytearray(image_bytes)
        
        positive_reviews_data = zipfile.ZipInfo(negative_reviews_filename)
        positive_reviews_data.date_time = time.localtime(time.time())[:6]
        positive_reviews_data.compress_type = zipfile.ZIP_STORED
        zipf.writestr(positive_reviews_data, image_bytes)
        
        image_bytes = open(os.path.join(basedir, filename_positive), "rb").read()
        image_bytes = bytearray(image_bytes)
        
        positive_reviews_data = zipfile.ZipInfo(positive_reviews_filename)
        positive_reviews_data.date_time = time.localtime(time.time())[:6]
        positive_reviews_data.compress_type = zipfile.ZIP_STORED
        zipf.writestr(positive_reviews_data, image_bytes)
    memory_file.seek(0)
    return send_file(memory_file, 
                    mimetype='zip', 
                    attachment_filename=zip_name,
                    as_attachment=True)


    # TODO: use the real reviews
    hotel_id = request.args.get('hotel_id')
    if not hotel_id:
        return ''
    
    booking_service = BookingService()
    all_reviews = booking_service.get_reviews(hotel_id)
    positive_reviews = booking_utils.extract_positive_reviews(all_reviews)
    negative_reviews = booking_utils.extract_negative_reviews(all_reviews)
    
    if not positive_reviews and not negative_reviews:
        return ''

    # Creates wordcloud for positive reviews.    
    positive_reviews_filename = os.path.dirname(os.path.abspath(__file__)) + '/' + str(hotel_id) + '_positive_reviews_wordcloud'
    create_wordcloud(positive_reviews, positive_reviews_filename)
    positive_reviews_filename += '.png'

    # Creates wordcloud for negative reviews.
    negative_reviews_filename = os.path.dirname(os.path.abspath(__file__)) + '/' + str(hotel_id) + '_negative_reviews_wordcloud'
    create_wordcloud(negative_reviews, negative_reviews_filename)
    negative_reviews_filename += '.png'
    
    # Sends the result as a zip file
    zip_name = str(hotel_id) + '_reviews.zip'
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', compression=zipfile.ZIP_STORED) as zipf:
        # Positive reviews wordcloud.
        image_bytes = open(os.path.join(basedir, positive_reviews_filename), "rb").read()
        image_bytes = bytearray(image_bytes)
        
        positive_reviews_data = \
            zipfile.ZipInfo(os.path.basename(positive_reviews_filename))
        positive_reviews_data.date_time = time.localtime(time.time())[:6]
        positive_reviews_data.compress_type = zipfile.ZIP_STORED
        zipf.writestr(positive_reviews_data, image_bytes)

        # Negative reviews wordcloud.
        image_bytes = open(os.path.join(basedir, negative_reviews_filename), "rb").read()
        image_bytes = bytearray(image_bytes)
       
        negative_reviews_data = \
            zipfile.ZipInfo(os.path.basename(negative_reviews_filename))
        negative_reviews_data.date_time = time.localtime(time.time())[:6]
        negative_reviews_data.compress_type = zipfile.ZIP_STORED
        zipf.writestr(negative_reviews_data, image_bytes)
    memory_file.seek(0)
    return send_file(memory_file, 
                    mimetype='zip', 
                    attachment_filename=zip_name,
                    as_attachment=True)


def get_analyzer(holiday_plan_id):
    if HolidayPlan.query.filter_by(id=holiday_plan_id).scalar() is None:
        return Analyzer()        
    analyzer_as_json = \
        HolidayPlan.query.filter_by(id=holiday_plan_id).first().analyzer_as_json
    return Analyzer().from_json(analyzer_as_json)


def save_analyzer(holiday_plan_id, analyzer):
    HolidayPlan.query.filter_by(id=holiday_plan_id).delete()
    holiday_plan = HolidayPlan(id=holiday_plan_id, analyzer_as_json=analyzer.to_json())
    db.session.add(holiday_plan)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()

    app.run()
