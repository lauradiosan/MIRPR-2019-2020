"""An analyzer for analyzing the raw input text."""
import logging

from copy import deepcopy

import en_core_web_sm
from word2number import w2n

import dateutil.parser as dparser

import nltk
from nltk.stem import LancasterStemmer, WordNetLemmatizer

import analyzer.nltk_utils as nltk_utils
import analyzer.time_utils as time_utils

from analyzer.vacation_requirements import VacationRequirements

import analyzer.image_classifier_config as IMAGE_CLASSIFIER_CONFIG

from image_classifier.image_classifier import ImageClassifier
from image_classifier.image_type import ImageType

NLP = en_core_web_sm.load()


class Analyzer:
    """Analyzes and extracts information from text."""
    def __init__(self):
        self.__text = []
        self.__vacation_requirements = VacationRequirements()

        # tokens: https://stackoverflow.com/questions/29332851/what-does-nn-vbd-in-dt-nns-rb-means-in-nltk
        self.__grammar = ('''
            COUNT: {<CD><NNS>|<CD><JJ>*<NNS>|<CD>(<JJ><CC>)*<JJ><NNS>|<CD><NN>|<CD><JJ>*<NN>|<CD>(<JJ><CC>)*<JJ><NN>}
        ''')
        self.__chunk_parser = nltk.RegexpParser(self.__grammar)
        self.__stemmer = LancasterStemmer()
        self.__lemmatizer = WordNetLemmatizer()

        logging.basicConfig(format='%(asctime)-15s %(message)s')
        self.__logger = logging.getLogger('Analyzer')


    def to_json(self):
        json = {}
        json["text"] = self.__text
        json["vacation_requirements"] = self.__vacation_requirements.to_json()
        return json


    def from_json(self, json):
        self.__text = json['text']
        self.__vacation_requirements = \
            VacationRequirements().from_json(json['vacation_requirements'])
        return self


    def get_vacation_requirements(self):
        """Returns a deepcopy of self.__vacation_requirements"""
        return deepcopy(self.__vacation_requirements)


    def analyse(self, text):
        """Analyses the given text."""
        self.__text.append(text)

        doc = NLP(text)

        tokens = nltk.word_tokenize(text)
        tags = nltk.pos_tag(tokens)
        tree = self.__chunk_parser.parse(tags)

        if not self.__vacation_requirements.cities:
            self.__extract_locations(doc)
        if self.__vacation_requirements.start_date is None \
            or self.__vacation_requirements.end_date is None:
            self.__extract_dates(doc)
        if self.__vacation_requirements.number_of_rooms is None:
            self.__extract_number_of_rooms(tree)
        if self.__vacation_requirements.number_of_children is None:
            self.__extract_number_of_children(doc)


    def analyse_image(self, image_data, width, height):
        """Extract locations from the given image."""
        image_classifier = \
            ImageClassifier(saved_data_directory=IMAGE_CLASSIFIER_CONFIG.SAVED_DATA_DIRECTORY,
                            model_id=IMAGE_CLASSIFIER_CONFIG.MODEL_ID)
        image_classifier.load_model()
        image = image_classifier.image_bytes_as_numpy_array(image_data, width, height)
        image_type = image_classifier.classify(image)
        locations = self.__get_locations_from_image_type(image_type)
        self.__vacation_requirements.cities = locations


    def __get_locations_from_image_type(self, image_type):
        """Get locations that match the given image type."""
        locations = {
            ImageType.FOREST: ['New York'],
            ImageType.SAND_BEACH: ['Athens'],
            ImageType.SNOW_MOUNTAIN: ['Zermatt'],
        }
        return locations[image_type]


    def __extract_locations(self, doc):
        """Extracts the locations from the text and sets the cities list."""
        # GPE =	Geopolitical entity, i.e. countries, cities, states.
        self.__vacation_requirements.cities = \
            ([X.text for X in doc.ents if X.label_ == "GPE"])


    def __extract_dates(self, doc):
        """Extracts the dates from the text and sets start_date and end_date."""
        dates_list = ([X.text for X in doc.ents if X.label_ == "DATE"])

        if not dates_list:
            return
        if len(dates_list) == 1 or len(dates_list) == 2:
            dates = []
            for item in time_utils.timesplit(dates_list[0] if len(dates_list) == 1 \
                else dates_list[0] + " and " + dates_list[1]):
                dates.append(dparser.parse(item))
            if len(dates) != 2:
                self.__logger.warning(
                    "Could not extract start_date and end_date. " +
                    "Invalid number of dates: %s.", len(dates))
                return

            self.__vacation_requirements.start_date = dates[0]
            self.__vacation_requirements.end_date = dates[1]
            if self.__vacation_requirements.start_date > self.__vacation_requirements.end_date:
                self.__vacation_requirements.start_date, self.__vacation_requirements.end_date = \
                self.__vacation_requirements.end_date, self.__vacation_requirements.start_date

            self.__vacation_requirements.start_date = \
                str(self.__vacation_requirements.start_date.year) + "-" + \
                str(self.__vacation_requirements.start_date.month) + "-" + \
                str(self.__vacation_requirements.start_date.day)
            self.__vacation_requirements.end_date = \
                str(self.__vacation_requirements.end_date.year) + "-" + \
                str(self.__vacation_requirements.end_date.month) + "-" + \
                str(self.__vacation_requirements.end_date.day)

            return
        self.__logger.warning(
            "Could not extract start_date and end_date. " +
            "Invalid number of dates: %s.", len(dates_list))


    # Not used anymore. delete later
    def __extract_number_of_rooms_old(self, doc):
        """Extract the number of rooms from the text and sets number_of_rooms."""
        # TODO. chiar fa asta
        numbers = ([X.text for X in doc.ents if X.label_ == "CARDINAL"])
        if not numbers:
            self.__vacation_requirements.number_of_rooms = None
            return
        try:
            self.__vacation_requirements.number_of_rooms = w2n.word_to_num(numbers[0])
        except:
            logging.error("Failed to extract number.")


    def __extract_number_of_rooms(self, tree):
        """Extract the number of rooms from the text and sets number_of_rooms.

        TODO explain duplicate"""
        count_nodes = nltk_utils.get_nodes(tree, 'COUNT')
        room_subject = ['room']
        room_nodes = []
        for count_node in count_nodes:
            if nltk_utils.is_node_about_subject(count_node, room_subject, self.__stemmer):
                room_nodes.append(count_node)

        for room_node in room_nodes:
            cardinal_number_or_none = \
                nltk_utils.extract_cardinal_number(room_node)
            if cardinal_number_or_none is not None:
                self.__vacation_requirements.number_of_rooms = \
                    w2n.word_to_num(cardinal_number_or_none)
                return


    def __extract_number_of_children(self, doc):
        """Extract the number of children from the text and sets number_of_children.

        TODO explain duplicate"""
        children_subject = ['kid', 'child']
        cardinal_number_or_none = \
            nltk_utils.extract_number_of_subject(doc, children_subject, self.__lemmatizer)
        if cardinal_number_or_none is not None:
            self.__vacation_requirements.number_of_children = \
                w2n.word_to_num(cardinal_number_or_none)
