from backend.db_access import DbAccess
from flask_socketio import SocketIO
from time import time
from random import randrange


class SocketController:

    def __init__(self, socket_io: SocketIO, db_access: DbAccess):
        self.socket_io = socket_io
        self.db_access = db_access
        self.current_session = None

    def message_handler(self, session_id):
        """
        :param session_id: the current session_id
        :return:
        """
        emotion = randrange(0, 7)
        self.db_access.add_session_details(session_id, emotion, -1)

    def start_session_handler(self):
        current_session = self.db_access.add_session(time() * 1000, "generatedSession" + str(time() * 1000))
        self.current_session = current_session
        self.socket_io.emit('session_started', current_session.id, broadcast=True)
        return current_session

    def stop_session_handler(self):
        new_session = self.db_access.set_end_time_for_session(self.current_session.id, time() * 1000)
        self.socket_io.emit('session_stopped', broadcast=True)
        return new_session
