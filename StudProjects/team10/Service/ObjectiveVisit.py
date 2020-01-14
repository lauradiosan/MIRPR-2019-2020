from API.ItineraryAPI.Location import Location


class ObjectiveVisit:
    def __init__(self, location: Location, staying_time, priority, no_of_reviews, tripadvisor_link, description):
        self.description = description
        self.tripadvisor_link = tripadvisor_link
        self.no_of_reviews = no_of_reviews
        self.location = location
        self.staying_time = staying_time
        self.priority = priority

    def toString(self):
        return " [ : "+str(self.location)+" || "+str(self.no_of_reviews)+" || "+\
               str(self.staying_time)+" || "+str(self.description)+ "|| "+str(self.tripadvisor_link)+" ] "