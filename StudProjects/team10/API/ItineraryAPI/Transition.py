class Transition:
    def __init__(self, distance, duration):
        """
        Creates a transition item
        :param distance: Distance of transition with respect to traffic navigation
        :param duration: Duration of transition with respect to traffic navigation
        """
        self.__distance = distance
        self.__duration = duration

    @property
    def distance(self):
        return self.__distance

    @property
    def duration(self):
        return self.__duration

    def __str__(self) -> str:
        return "Distance: " + str(self.__distance) + "\nDuration: " + self.__duration