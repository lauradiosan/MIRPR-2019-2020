from backend.db_access import DbAccess


class RestController:

    def __init__(self, db_access: DbAccess):
        self.db_access = db_access

    def get_sessions_handler(self):
        sessions = self.db_access.select_all_sessions()
        return sessions

    def get_session_details_emotions_handler(self, session_id):
        session_details = self.db_access.get_session_details_for_session(session_id)
        return session_details

    def get_image_for_session_and_second(self, session_id, video_time_stamp):
        image = self.db_access.get_image_for_session_and_second(session_id, video_time_stamp)
        return image
