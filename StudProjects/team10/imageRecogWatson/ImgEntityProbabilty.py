class ImgObj:
    def __init__(self,entity,prob):
        self.entity = entity
        self.prob =prob

    def getEntity(self):
        return self.entity

    def getProb(self):
        return self.prob

    def __str__(self):
        return str(self.entity) + " " + str(self.prob)