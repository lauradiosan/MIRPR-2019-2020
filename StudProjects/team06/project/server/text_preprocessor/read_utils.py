"""Utils for reading stopwords."""
import os
from os.path import dirname

DEFAULT_STOPWORDS_FILE = os.path.join(dirname(__file__), 'stopwords.txt')
HOTEL_SPECIFIC_STOPWORDS_FILE = \
    os.path.join(dirname(__file__), 'hotels_specific_stopwords.txt')
KEYWORDS_STOPWORDS_FILE = \
    os.path.join(dirname(__file__), 'keywords_specific_stopwords.txt')


def read_stopwords(logger=None, filename=DEFAULT_STOPWORDS_FILE):
    """Reads the stopwords from the given file.

    Uses default values if no file was given."""
    stopwords = []
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            stopwords = stopwords + [line.rstrip('\n')]
        f.close()
    except Exception as e:
        if logger is not None:
            logger.exception('Failed to read the stopwords from %s: ', filename, e)
    return stopwords


def read_hotel_specific_stopwords(logger=None, filename=HOTEL_SPECIFIC_STOPWORDS_FILE):
    """Reads the stopwords from the given file and DEFAULT_STOPWORDS_FILE.

    Uses default values if no file was given."""
    return read_stopwords(logger) + read_stopwords(logger, filename)


def read_kewyords_stopwords(logger=None, filename=KEYWORDS_STOPWORDS_FILE):
    """Reads the stopwords from the given file and KEYWORDS_STOPWORDS_FILE.

    Uses default values if no file was given."""
    return read_stopwords(logger) + read_stopwords(logger, filename)

