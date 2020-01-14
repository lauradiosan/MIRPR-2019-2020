"""A class grouping all the vacation requirements."""

class VacationRequirements:
    """A class grouping all the vacation requirements."""
    def __init__(self):
        self.cities = []
        self.start_date = None
        self.end_date = None
        self.number_of_guests = 1
        self.number_of_rooms = None
        self.number_of_children = None


    def to_json(self):
        """Converts the VacationRequirements object to json."""
        json = {}
        json['cities'] = self.cities
        json['start_date'] = self.start_date
        json['end_date'] = self.end_date
        json['number_of_guests'] = self.number_of_guests
        json['number_of_rooms'] = self.number_of_rooms
        json['number_of_children'] = self.number_of_children
        return json


    def from_json(self, json):
        """Populates the VacationRequirements object from json."""
        self.cities = json['cities']
        self.start_date = json['start_date']
        self.end_date = json['end_date']
        self.number_of_guests = json['number_of_guests']
        self.number_of_rooms = json['number_of_rooms']
        self.number_of_children = json['number_of_children']
        return self


    def are_all_required_set(self):
        """Checks whether all required fields are valid."""
        return self.cities and self.start_date and self.end_date \
            and self.number_of_rooms and self.number_of_children
