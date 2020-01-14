from API.ItineraryAPI import Location


class Visit:
    def __init__(self, location: Location, start_time, end_time):
        """
        Creates a visit for a location
        :param location: Location to be visited
        :param start_time: Start time of the visit (must be "YYYY-MM-DDThh:mm:ss" format)
        :param end_time: End time of the visit (must be "YYYY-MM-DDThh:mm:ss" format)
        """
        self.__location = location
        self.__start_time = start_time
        self.__end_time = end_time

    @property
    def location(self):
        return self.__location

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    def __str__(self) -> str:
        return "Location: " + self.__location.name + " " + str(self.__location.latitude) + " " + str(self.__location.longitude) + "\nFrom: " + self.__start_time + " To: " + self.__end_time

