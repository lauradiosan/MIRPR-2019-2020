import requests

from services.vacation_requirements import VacationRequirements

from PIL import Image as PILImage

from io import BytesIO


class HolidayChatbotService:
    def reset(self):
        try:
            url = self.__build_url('reset')
            response = requests.request('GET', 
                                        url, 
                                        headers=self.__HEADERS,
                                        cookies=self.__COOKIES)
            return ''
        except Exception as e:
            print(e)
            return None


    def analyze_text(self, text):
        """TODO

        Returns vacation_requirements."""
        url = self.__build_url('analyze-text')
        querystring = {
            'input_text': text,
        }
        try:
            response = requests.request('POST', 
                                        url, 
                                        headers=self.__HEADERS, 
                                        cookies=self.__COOKIES,
                                        params=querystring)
            if response.status_code != 200:
                return None

            vacation_requirements_as_json = response.json()
            vacation_requirements = VacationRequirements()
            vacation_requirements.from_json(vacation_requirements_as_json)
            return vacation_requirements
        except Exception as e:
            print(e)
            return None


    def analyse_image(self, image):
        """TODO"""
        url = self.__build_url('analyze-image')
        try:
            image_data = image.read()
            pil_image = PILImage.open(BytesIO(image_data))
            width, height = pil_image.size
            querystring = {
                'width': width,
                'height': height,
            }
            response = requests.request('POST', 
                                        url, 
                                        headers=self.__HEADERS, 
                                        cookies=self.__COOKIES,
                                        data=image_data,
                                        params=querystring)
            if response.status_code != 200:
                return None

            vacation_requirements_as_json = response.json()
            vacation_requirements = VacationRequirements()
            vacation_requirements.from_json(vacation_requirements_as_json)
            return vacation_requirements
        except Exception as e:
            print(e)
            return None


    def get_hotels_list(self):
        """TODO"""
        try:
            url = self.__build_url('hotels-list')
            response = requests.request('GET', 
                                        url, 
                                        headers=self.__HEADERS,
                                        cookies=self.__COOKIES)
            if response.status_code != 200:
                return []

            hotels_list_as_json = response.json().get('result', [])
            return hotels_list_as_json
        except Exception as e:
            print(e)
            return []


    def get_hotel_reviews_wordcloud(self, hotel_id):
        """TODO

        Returns the image in bytes."""
        try:
            url = self.__build_url('hotel-reviews-wordcloud')
            querystring = {
                'hotel_id': hotel_id,
            } 
            response = requests.request('GET', 
                                        url, 
                                        headers=self.__HEADERS ,
                                        cookies=self.__COOKIES,
                                        params=querystring)
            if response.status_code != 200:
                None

            return response.content
        except Exception as e:
            print(e)
            return None


    def __build_url(self, path):
        return self.__BASE_URL + ':' + self.__PORT + '/' + path


    __BASE_URL = 'http://127.0.0.1'
    __PORT = '5000'
    __HEADERS = {'Content-Type': 'application/json; application/zip',
                 'charset': 'UTF-8',}
    __COOKIES = {'holiday_plan_id': '9ebbd0b25760557393a43064a92bae539d962103'}
