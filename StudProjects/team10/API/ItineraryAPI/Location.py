import json
import urllib

import dateutil.parser
import calendar
import requests




class Location:
    def __init__(self, name, latitude, longitude, country=None, city=None, street=None, schedule=None):
        """
        Creates a location
        :param name: Desired name for location
        :param latitude: Latitude of location
        :param longitude: Longitude of location
        :param country: Country of location
        :param city: City of location
        :param street: Street of location
        :param schedule: A dictionary with keys being days of the week (like "Wednesday") and values being a list of hours
        """
        self.__name = name
        self.__longitude = longitude
        self.__latitude = latitude
        self.__country = country or ""
        self.__city = city or ""
        self.__street = street or ""
        self.__schedule = schedule

    @property
    def name(self):
        return self.__name

    @property
    def longitude(self):
        return self.__longitude

    @property
    def latitude(self):
        return self.__latitude

    @property
    def country(self):
        return self.__country

    @property
    def city(self):
        return self.__city

    @property
    def street(self):
        return self.__street

    def is_closed(self, date):
        date = dateutil.parser.parse(date)
        len_sch = len(self.__schedule[calendar.day_name[date.weekday()]]) if self.__schedule else 0
        return len_sch == 1

    def opening_time(self, date):
        date = dateutil.parser.parse(date)
        len_sch = len(self.__schedule[calendar.day_name[date.weekday()]]) if self.__schedule else 0
        if len_sch == 0:
            return '00:00:00'
        elif len_sch == 1:
            return 'closed'
        else:
            return self.__schedule[calendar.day_name[date.weekday()]][0]

    def closing_time(self, date):
        date = dateutil.parser.parse(date)
        len_sch = len(self.__schedule[calendar.day_name[date.weekday()]]) if self.__schedule else 0
        if len_sch == 0:
            return '23:59:59'
        elif len_sch == 1:
            return 'closed'
        else:
            return self.__schedule[calendar.day_name[date.weekday()]][1]

    @staticmethod
    def __get_schedule(location):
        schedule = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'Sunday': []
        }
        if 'hours' in location:
            for h in location['hours']:
                day = ""
                if 'mon' in h['key']:
                    day = 'Monday'
                if 'tue' in h['key']:
                    day = 'Tuesday'
                if 'wed' in h['key']:
                    day = 'Wednesday'
                if 'thu' in h['key']:
                    day = 'Thursday'
                if 'fri' in h['key']:
                    day = 'Friday'
                if 'sat' in h['key']:
                    day = 'Saturday'
                if 'sun' in h['key']:
                    day = 'Sunday'
                schedule[day].append(h['value'])
        return schedule

    @staticmethod
    def get_locations_by_query(query_str, city=None):
        headers = {'content-type': 'application/json'}
        query_str = urllib.parse.quote(query_str)
        response = requests.get(settings.LOCATIONS % (query_str, settings.FACEBOOK_API_KEY), headers=headers)
        if response.status_code != 200: return []
        locations = json.loads(response.text)
        locations_list = []
        for l in locations['data']:
            schedule = Location.__get_schedule(l)
            location = Location(l['name'],
                                           l['location']['latitude'],
                                           l['location']['longitude'],
                                           l['location']['country'] if 'country' in l['location'] else "",
                                           l['location']['city'] if 'city' in l['location'] else "",
                                           l['location']['street'] if 'street' in l['location'] else "",
                                           schedule)
            if city and location.city != city:
                continue
            locations_list.append(location)
        return locations_list

    def __eq__(self, o: object) -> bool:
        if o is not Location: return False
        return self.latitude == o.latitude and self.longitude == o.longitude

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __str__(self) -> str:
        return self.__name + " " + str(self.__latitude) + " " + str(self.__longitude)

