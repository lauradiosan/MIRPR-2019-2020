from tinydb import TinyDB, Query

class Repository:
    def __init__(self):
        self.db = TinyDB('./controller/db.json')
    
    def get_all(self):
        parking_spots = self.db.all()
        return parking_spots

