class TextObj:
    def __init__(self, entities, location, date, budget):
        self.entities = entities
        self.location = location
        self.date = date
        self.budget = budget

    def getListOfObjectsWithProb(self):
        return self.entities

    def getLocation(self):
        return self.location

    def getDate(self):
        return self.date

    def getBudget(self):
        return self.budget

    def setEntities(self, entities):
        self.entities = entities

    def setLocation(self, location):
        self.location = location

    def setDate(self, date):
        self.date = date

    def setBudget(self, budget):
        self.budget = budget

    def __str__(self):
        return str(self.entities) + " " + str(self.location) + " " + str(self.date) + " " + str(self.budget)
