import json
import requests

import settings
from API.ItineraryAPI.Location import Location
from API.ItineraryAPI.Transition import Transition
from API.ItineraryAPI.Visit import Visit


class TravelItinerary:
    def __init__(self, start_date_time, end_date_time, start_location: Location, end_location: Location = None):
        """
        Creates a travel itinerary
        :param start_date_time: Start time of the travel (must be "YYYY-MM-DDThh:mm:ss" format)
        :param end_date_time: End time of the travel (must be "YYYY-MM-DDThh:mm:ss" format)
        :param start_location: Location where the travel starts
        :param end_location: Location where the travel ends
        """
        if start_date_time.split("T")[0] != end_date_time.split("T")[0]:
            raise ValueError("Trip must end the same day it started!")

        self.__start_date_time = start_date_time
        self.__end_date_time = end_date_time
        self.__start_location = start_location
        self.__end_location = end_location or start_location
        self.__visits = []
        self.__to_visit = []
        self.__agents = [{
            'name' : 'travelPlanner',
            "shifts": [
                {
                    "startTime": start_date_time,
                    "startLocation": {
                        "latitude": self.__start_location.latitude,
                        "longitude": self.__start_location.longitude
                    },
                    "endTime": end_date_time,
                    "endLocation": {
                        "latitude": self.__end_location.latitude,
                        "longitude": self.__end_location.longitude
                    }
                }
            ]
        }]
        self.__modified = True
        self.__cached = None

    def add_visit(self, location: Location, staying_time, priority):
        """
        Adds a visit to a location specifying the details. If opening and closing are not specified, the location is open all the time
        :param location: Location to visit
        :param date_of_visit: Date of the visit (must be "YYYY-MM-DD" format)
        :param staying_time: Staying time of the visit (must be "hh:mm:ss" format)
        :param priority: A priority for scheduling this visit
        :param opening_time: Opening time of the location (must be "hh:mm:ss" format)
        :param closing_time: Closing time of the location (must be "hh:mm:ss" format)
        """
        date_of_visit = self.__date_of_itinerary()
        if location.is_closed(date_of_visit):
            return
        visit = {
            "name": location.name,
            "OpeningTime": date_of_visit + 'T' + location.opening_time(date_of_visit),
            "ClosingTime": date_of_visit + 'T' + location.closing_time(date_of_visit),
            "DwellTime": staying_time,
            "Priority": int(priority),
            "Location": {
                "Latitude": location.latitude,
                "Longitude": location.longitude
            }
        }
        self.__to_visit.append(visit)
        self.__modified = True

    def __date_of_itinerary(self):
        return self.__start_date_time.split("T")[0]

    def __get_transitions(self, instructions):
        return [Transition(i['distance'], i['duration']) for i in instructions if i['instructionType'] == 'TravelBetweenLocations']

    def __get_visits(self, instructions):
        return [Visit(Location(i['itineraryItem']['name'],
                               i['itineraryItem']['location']['latitude'],
                               i['itineraryItem']['location']['longitude']),
                      i['startTime'], i['endTime']) for i in instructions if i['instructionType'] == 'VisitLocation']

    def __build_map_waypoint(self, location: Location, index):
        prefix = ""
        if index > 1:
            prefix = "&"
        index = str(index)
        return prefix + settings.MAP_WAYPOINT % (index, location.latitude, location.longitude, index)

    def compute_route(self):
        """
        Computes the travel itinerary
        :return: 2 lists: one of visits and one of transitions. At each index in visit, in the corresponding item from transition resides the transition from previous visit to the current one
        """
        if self.__modified and self.__cached == None:
            #print("Server req")
            requestJSON = {
                'agents' : self.__agents,
                'itineraryItems' : self.__to_visit
            }
            requestJSON = json.dumps(requestJSON)
            headers = {'content-type': 'application/json'}

            print("THE REQUEST :\n"+ str(requestJSON) , str(headers))

            response = requests.post(settings.OPTIMIZE_ITINERARY % settings.MICROSOFT_API_KEY, data=requestJSON, headers=headers)
            if response.status_code >= 400 and response.status_code < 500:
                print("THE RESPONSE:\n "+response.text)
                raise ValueError("Bad request or cannot schedule the desired itinerary within the given period")
            if response.status_code >= 500:
                raise ValueError("The server encountered issues")
            itinerary = json.loads(response.text)
            print(response.text)
            self.__cached = itinerary
            self.__modified = False
        else:
            itinerary = self.__cached
        instructions = itinerary['resourceSets'][0]['resources'][0]['agentItineraries'][0]['instructions']
        return self.__get_visits(instructions), self.__get_transitions(instructions)

    def compute_route_and_get_map(self):
        """
        Computes the travel itinerary and returns it alongside a map containing the planned itinerary
        :return: 2 lists: one of visits and one of transitions. At each index in visit, in the corresponding item from transition resides the transition from previous visit to the current one.
        Returns also a stream corresponding to an image of a map with scheduled visits
        """
        visits, transitions = self.compute_route()
        waypoints = self.__build_map_waypoint(self.__start_location, 1) + self.__build_map_waypoint(self.__end_location, len(visits) + 2)
        for i in range(len(visits)):
            waypoints += self.__build_map_waypoint(visits[i].location, i + 2)
        response = requests.get(settings.GET_MAP % (waypoints, settings.MICROSOFT_API_KEY), stream=True)
        if response.status_code >= 400 and response.status_code < 500:
            raise ValueError("Bad request or cannot schedule the desired itinerary within the given period")
        if response.status_code >= 500:
            raise ValueError("The server encountered issues")
        return visits, transitions, response.raw

