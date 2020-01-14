"""Methods for Booking API: https://rapidapi.com/apidojo/api/booking/endpoints"""
import requests

from .review import Review

from os.path import dirname
  
import imp

api_keys = imp.load_source('api_keys', dirname(__file__) + '/../api_keys.py')


class BookingService:
    def __init__(self):
        self.__headers = {
            'x-rapidapi-host': "apidojo-booking-v1.p.rapidapi.com",
            'x-rapidapi-key': api_keys.RAPIDAPI_KEY
        }


    def get_hotels_list(self, requirements):
        """Returns the list of hotels that meet the given requirements.

        If the request fails, returns an empty list.

        Args:
          requirements: of type VacationRequirements
        """
        try:
            dest_ids = [self.get_dest_id(city) for city in requirements.cities]
            url = "https://apidojo-booking-v1.p.rapidapi.com/properties/list"
            querystring = {
                "price_filter_currencycode":"USD",
                "travel_purpose": "leisure",
                "categories_filter": "price::9-40,free_cancellation::1,class::1,class::0,class::2",
                "search_id": "none",
                "order_by": "popularity",
                "languagecode": "en-us",
                "children_qty": str(requirements.number_of_children),
                "children_age": "5,7",
                "search_type": "city",
                "offset": "0",
                "dest_ids": dest_ids,
                "guest_qty": str(requirements.number_of_guests),
                "arrival_date": requirements.start_date,
                "departure_date": requirements.end_date,
                "room_qty": str(requirements.number_of_rooms)
            }

            response = requests.request("GET", url, headers=self.__headers, params=querystring)
            # return response.json().get('result', [])
            return response.json()
        except Exception as e:
            print(e)
            return []


    def get_reviews(self, hotel_id):
        """TODO

        Args:
            hotel_id: the id of the hotel for which to return the reviews
        """
        try:
            url = "https://apidojo-booking-v1.p.rapidapi.com/reviews/list"
            offset = 0
            result = []
            new_partial_result = []

            while offset == 0 or new_partial_result:
                querystring = {
                    "languagecode": "en-us",
                    "offset": str(offset),
                    "filter_language": "en",
                    "rows": "50",
                    "hotel_ids": hotel_id
                }
                offset += 50

                response = requests.request("GET", url, headers=self.__headers, params=querystring)
                new_partial_result = response.json().get('result', [])
                result = result + new_partial_result

            result = [R for R in result if R['pros'] or R['cons']]
            return result
        except Exception as e:
            print(e)
            return []


    def get_formatted_reviews(self, hotel_id):
        """TODO

        Returns the reviews as a list of Review objects.

        Args:
            hotel_id: the id of the hotel for which to return the reviews
        """
        try:
            all_reviews = self.get_reviews(hotel_id)
            reviews = [self.__create_review_object(R) for R in all_reviews]
            return reviews
        except Exception as e:
            print(e)
            return 


    def extract_links_from_hotels_list(self, hotels_list):
        """Returns the links from the given hotels list."""
        links_list = [hotel["url"] for hotel in hotels_list]
        return links_list


    def get_dest_id(self, text):
        try:
            """Makes a request to get the dest_ids for the given location."""
            url = "https://apidojo-booking-v1.p.rapidapi.com/locations/auto-complete"
            querystring = {"languagecode": "en-us", "text": text}

            response = requests.request("GET", url, headers=self.__headers, params=querystring)
            return response.json()[0]["dest_id"]
        except Exception as e:
            print(e)
            return []


    def __get_date_as_string(self, date):
        """Converts the given date to a string."""
        return str(date.year) + "-" + str(date.month) + "-" + str(date.day)


    def __create_review_object(self, json):
        r = Review()
        r.positive_review = json['pros'] or ''
        r.negative_review = json['cons'] or ''
        return r


if __name__ == '__main__':
    bs = BookingService()
    hotel_id = '435027'
    # result = bs.get_positive_reviews(hotel_id)
    result = bs.get_formatted_reviews(hotel_id)
    print(result)
    print('number of reviews: %d' % len(result))
