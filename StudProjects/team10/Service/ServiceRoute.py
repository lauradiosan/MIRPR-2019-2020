import pathlib
import re
from os import listdir
import os

from API.ItineraryAPI.Location import Location
from API.ItineraryAPI.TravelItinerary import TravelItinerary
import geocoder
import pkgutil

from Service.ObjectiveVisit import ObjectiveVisit


class ServiceRoute:
    def __init__(self):
        pass

    def configureDestionationDetails(self, city):
        '''
        Usage: this if for when user selected his desired destination and proceeds to planning the route
        :param city:
        :return:
        '''
        self.__city = city

    def configureRouteDetails(self, start_date_time, end_date_time, start_location: Location, end_location: Location = None):
        '''
        Usage: this is for when user is configuring his details for the itinerary (for instance, through a for,
        where he sets these aspects.
        :param start_date_time:
        :param end_date_time:
        :param start_location: this will be retrieved through getLocationFromCity or getCurrentLocation prior to this call
        :param end_location: this will be retrieved through getLocationFromCity or getCurrentLocation prior to this call
        :return:
        '''
        self.__start_date_time = start_date_time
        self.__end_date_time = end_date_time
        self.__start_location = start_location
        self.__end_location = end_location
        self.__travelItinerary = TravelItinerary(start_date_time, end_date_time, start_location, end_location)

    def getLocationFromCity(self, location_query):
        '''
        Usage: this is for when user is s
        :param location_query:
        :return:
        '''
        return Location.get_locations_by_query(location_query, self.__city)

    def getCurrentLocation(self):
        g = geocoder.ip('me')
        print(str(g.latlng[0])+"--"+ str(g.latlng[1]))
        return Location('start', g.latlng[0], g.latlng[1])

    def __build_schedule(self, schedule):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        days_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        built_schedule = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'Sunday': []
        }
        days_full = list(built_schedule.keys())
        sw = 0
        for i in range(0, len(schedule), 2):
            day_interval = schedule[i].split('-')
            if len(day_interval) == 2:
                start_idx = days.index(day_interval[0].strip())
                stop_idx = days.index(day_interval[1].strip())
                if stop_idx < start_idx:
                    start_idx, stop_idx = stop_idx, start_idx
                for day_idx in range(start_idx, stop_idx + 1):
                    day = days_full[day_idx]
                    open_close = schedule[i + 1].split('-')
                    if len(open_close) != 2:
                        # print(open_close)
                        raise ValueError("Invalid schedule")
                    hour = ""
                    if 'AM' in open_close[0]:
                        hour = open_close[0][0:-3].strip() + ":00"
                    else:
                        hour = open_close[0][0:-3].strip()
                        h = int(hour.split(':')[0])
                        h = h + 12 if h < 12 else h
                        hour = str(h) + ":" + hour.split(':')[1] + ":00"

                    built_schedule[day].append(hour)
                    if 'AM' in open_close[1]:
                        hour = open_close[1][0:-3] + ":00"
                    else:
                        hour = open_close[1][0:-3]
                        h = int(hour.split(':')[0])
                        h = h + 12 if h < 12 else h
                        hour = str(h) + ":" + hour.split(':')[1] + ":00"

                    built_schedule[day].append(hour)
                    sw = 1
            elif len(day_interval) == 1:
                day_idx = days.index(day_interval[0].strip())
                day = days_full[day_idx]
                open_close = schedule[i + 1].split('-')
                if len(open_close) != 2:
                    # print(open_close)
                    raise ValueError("Invalid schedule")
                hour = ""
                if 'AM' in open_close[0]:
                    hour = open_close[0][0:-3].strip() + ":00"
                else:
                    hour = open_close[0][0:-3].strip()
                    h = int(hour.split(':')[0])
                    h = h + 12 if h < 12 else h
                    hour = str(h) + ":" + hour.split(':')[1] + ":00"

                built_schedule[day].append(hour)
                if 'AM' in open_close[1]:
                    hour = open_close[1][0:-3] + ":00"
                else:
                    hour = open_close[1][0:-3]
                    h = int(hour.split(':')[0])
                    h = h + 12 if h < 12 else h
                    hour = str(h) + ":" + hour.split(':')[1] + ":00"

                built_schedule[day].append(hour)
                sw = 1
        if sw == 1:
            for day in days_full:
                if len(built_schedule[day]) == 0:
                    built_schedule[day].append("closed")
        #print(schedule)
        #print(built_schedule)
        return built_schedule

    def __nr_to_hour(self, nr):
        hour = int(nr)
        minutes = int((nr - hour) * 60)
        hour = str(hour)
        if len(hour) == 1: hour = "0" + hour
        minutes = str(minutes)
        if len(minutes) == 1: minutes = "0" + minutes
        return hour+":"+minutes+":00"


    def __parseFilterFile(self, filter):
        objectives = []
        goodPath = str(pathlib.Path(__file__).parent.parent.absolute()) + "\\Scrapping\\obiectiveData\\" + filter + ".txt"

        with open(goodPath.replace('\\','/'),encoding="utf-8") as file:
            for line in file:
                data = line.strip().split(";")
                if len(data[-2]) == 0 or len(data[-3]) == 0:
                    continue
                try:
                    schedule = eval(data[-5])
                    if len(schedule) % 2 == 1:
                        continue
                    if 'hour' not in data[-4]:
                        continue
                    schedule = self.__build_schedule(schedule)
                except Exception as e:
                    # print(e)
                    continue
                nrs = re.findall(r'\d+', data[-4])
                if len(nrs) > 3 or len(nrs) == 0:
                    continue
                s = 0
                for nr in nrs:
                    s += int(nr)
                location = Location(data[0], float(data[-3]), float(data[-2]), schedule=schedule)
                if location.is_closed(self.__start_date_time.split("T")[0]):
                    continue
                objectives.append(ObjectiveVisit(location, self.__nr_to_hour(s / len(nr)), None, data[1], data[3], data[5]))
        return objectives

    def getObjectivesByLocationAndFilter(self,location, filters):
        objectives = []
        for filter in filters:
            objectives.extend(self.__parseFilterFile(filter))
        return objectives

    def getFilters(self):
        data = str(pathlib.Path(__file__).parent.parent.absolute()) + "\Scrapping\obiectiveData"
        return [str(file).split(".txt")[0] for file in listdir(data)]

    def getRouteVisualization(self):
        return self.__map

    def getObjectivesVisitsRoute(self, objectivesVisits):
        '''
        Usage: after user gets objectives getObjectivesByLocationAndFilter through and selects his
        preferences (staying time, priority), this method will be used to compute the route
        :param objectivesVisits:
        :return:
        '''
        for objectivesVisit in objectivesVisits:
            self.__travelItinerary.add_visit(objectivesVisit.location,
                                             objectivesVisit.staying_time,
                                             objectivesVisit.priority)
        visits, tranz, self.__map = self.__travelItinerary.compute_route_and_get_map()

        return visits, tranz