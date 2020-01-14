from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Session(base):
    __tablename__ = 'sessions'
    id = Column(Integer, autoincrement=True, primary_key=True)
    upload_time_stamp = Column(Integer)
    name = Column(VARCHAR(length=50))

    def __repr__(self):
        return "<Session(id=%s, upload_time_stamp=%s, name=%s)>"\
               % (self.id, self.upload_time_stamp, self.name)
