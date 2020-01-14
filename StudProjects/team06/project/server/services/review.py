import uuid 
  

class Review:
    def __init__(self):
        self.id = str(uuid.uuid1().hex)
        self.positive_review = ""
        self.negative_review = ""


    def __repr__(self):
        return "Review %s [negative: %s, positive: %s]" % (self.id, self.positive_review, self.negative_review)
