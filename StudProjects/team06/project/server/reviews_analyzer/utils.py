"""Utils methods for Reviews Analyzer."""
import os

import tensorflow as tf
import tensorflow_hub as hub

from textblob import TextBlob

os.environ["TFHUB_CACHE_DIR"] = '/tmp/tfhub'

UNIVERSAL_SENTENCE_ENCODER_LINK = "https://tfhub.dev/google/universal-sentence-encoder/2"

# For cache: http://storage.googleapis.com/tfhub-modules/google/universal-sentence-encoder/2.tar.gz
# import hashlib
# print(hashlib.sha1(UNIVERSAL_SENTENCE_ENCODER_LINK.encode("utf8")).hexdigest())

embed = hub.Module(UNIVERSAL_SENTENCE_ENCODER_LINK)


def encode(data):
    """Encode the given data."""
    init_op = [tf.compat.v1.global_variables_initializer(),
               tf.compat.v1.tables_initializer()]
    session = tf.compat.v1.Session()
    session.run(init_op)
    embeddings = embed(data)
    encoded_data = session.run(embeddings)
    encoded_data = ([X for X in encoded_data])
    return encoded_data


def extract_hotels(dataset, key_column, info_columns=[]):
    """Returns the hotels together with additional info.

    Uses key_column as key.
    TODO: result type"""
    hotels = {}
    keys = dataset[key_column]
    # Remove duplicates.
    keys = list(dict.fromkeys(keys))
    for key in keys:
        entry = [(X) for _, X in dataset.iterrows()
                 if X[key_column] == key][0]
        info = []
        for info_column in info_columns:
            info = info + [entry[info_column]]
        hotels[key] = info
    return hotels


def calculate_sentiment_for_array(data):
    """Returns an array of float values, representing the sentiments."""
    sentiments = []
    for entry in data:
        data_as_textblod = TextBlob(entry)
        sentiment = data_as_textblod.sentiment.polarity
        sentiments.append(sentiment)
    return sentiments
