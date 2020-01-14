from sqlalchemy import Column, Integer, Float, BLOB
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class SessionDetails(base):
    __tablename__ = 'sessions_details'
    detail_id = Column(Integer, autoincrement=True, primary_key=True)
    session_id = Column(Integer)
    photo = Column(BLOB)
    dominant_emotion = Column(Integer)
    video_time_stamp = Column(Integer)
    angry_probability = Column(Float)
    disgust_probability = Column(Float)
    fear_probability = Column(Float)
    happy_probability = Column(Float)
    sad_probability = Column(Float)
    surprise_probability = Column(Float)
    neutral_probability = Column(Float)

    def __repr__(self):
        return "<SessionDetails(" \
               "detail_id=%s, " \
               "session_id=%s, " \
               "dominant_emotion=%s, " \
               "video_time_stamp=%s, " \
               "angry_probability=%s, " \
               "disgust_probability=%s, " \
               "fear_probability=%s, " \
               "happy_probability=%s, " \
               "sad_probability=%s, " \
               "surprise_probability=%s, " \
               "neutral_probability=%s, " \
               ")>"\
               % (self.detail_id,
                  self.session_id,
                  self.dominant_emotion,
                  self.video_time_stamp,
                  self.angry_probability,
                  self.disgust_probability,
                  self.fear_probability,
                  self.happy_probability,
                  self.sad_probability,
                  self.surprise_probability,
                  self.neutral_probability,
                  )
