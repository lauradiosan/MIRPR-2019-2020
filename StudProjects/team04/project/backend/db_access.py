import json

from sqlalchemy import MetaData, Table, Column, Integer, Float, BLOB, VARCHAR
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.session import Session
from backend.session_details import SessionDetails


class DbAccess:

    def __init__(self, db_engine):
        self.db_engine = db_engine
        self.db_session_factory = sessionmaker(bind=db_engine)
        if not db_engine.dialect.has_table(db_engine, "sessions"):
            metadata = MetaData(db_engine)
            Table("sessions", metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('upload_time_stamp', Integer),
                  Column('name', VARCHAR(length=50), default=None))
            metadata.create_all()
        if not db_engine.dialect.has_table(db_engine, "sessions_details"):
            metadata = MetaData(db_engine)
            Table("sessions_details", metadata,
                  Column('session_id', Integer, default=-1),
                  Column('photo', BLOB, default=None),
                  Column('dominant_emotion', Integer, default=-1),
                  Column('video_time_stamp', Integer, default=-1),
                  Column('angry_probability', Float, default=-1),
                  Column('disgust_probability', Float, default=-1),
                  Column('fear_probability', Float, default=-1),
                  Column('happy_probability', Float, default=-1),
                  Column('sad_probability', Float, default=-1),
                  Column('surprise_probability', Float, default=-1),
                  Column('neutral_probability', Float, default=-1),
                  Column('detail_id', Integer, primary_key=True, autoincrement=True))
            metadata.create_all()

    def select_all_sessions(self):
        """
        Query all rows in the tasks table
        :return: all the entries from the given table in json format
        """
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        rows = scoped_db_session.query(Session)
        return json.dumps(
            [{'id': session.id, 'upload_time_stamp': session.upload_time_stamp, 'name': session.name}
             for session in rows])

    def add_session(self, upload_time_stamp, name):
        new_session = Session(upload_time_stamp=upload_time_stamp, name=name)
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        scoped_db_session.add(new_session)
        scoped_db_session.commit()
        return new_session

    def add_full_session(self, upload_time_stamp, name):
        new_session = Session(upload_time_stamp=upload_time_stamp, name=name)
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        scoped_db_session.add(new_session)
        scoped_db_session.commit()
        return new_session

    def set_end_time_for_session(self, session_id, end_time_stamp):
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        new_session = scoped_db_session.query(Session).filter_by(id=session_id).first()
        new_session.end_time_stamp = end_time_stamp
        scoped_db_session.commit()
        return new_session

    def add_session_details(self, photo, session_id, dominant_emotion, video_time_stamp, prediction):
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        new_session_details = SessionDetails(
            session_id=session_id,
            photo=photo,
            dominant_emotion=dominant_emotion,
            video_time_stamp=video_time_stamp,
            angry_probability=prediction[0],
            disgust_probability=prediction[1],
            fear_probability=prediction[2],
            happy_probability=prediction[3],
            sad_probability=prediction[4],
            surprise_probability=prediction[5],
            neutral_probability=prediction[6],
        )
        scoped_db_session.add(new_session_details)
        scoped_db_session.commit()

    def get_session(self, session_id):
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        session = scoped_db_session.query(Session).get(session_id)
        return session

    def get_session_details_for_session(self, session_id):
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        rows = scoped_db_session.query(SessionDetails).filter_by(session_id=session_id)
        return json.dumps([
            {
                'emotion': session_det.dominant_emotion,
                'videoTimeStamp': session_det.video_time_stamp,
                'angryProbability': session_det.angry_probability,
                'disgustProbability': session_det.disgust_probability,
                'fearProbability': session_det.fear_probability,
                'happyProbability': session_det.happy_probability,
                'sadProbability': session_det.sad_probability,
                'surpriseProbability': session_det.surprise_probability,
                'neutralProbability': session_det.neutral_probability
            }
            for session_det in rows
        ])

    def get_image_for_session_and_second(self, session_id, video_time_stamp):
        current_db_session = scoped_session(self.db_session_factory)
        scoped_db_session = current_db_session()
        session_details = scoped_db_session.query(SessionDetails).filter_by(
            session_id=session_id,
            video_time_stamp=video_time_stamp
        )
        for detail in session_details:
            return detail.photo
        return None
