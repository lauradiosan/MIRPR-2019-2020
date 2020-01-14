"""Utils for creating wordclouds."""
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import logging
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from text_preprocessor.text_preprocessor import TextPreprocessor
from text_preprocessor import read_utils


def create_wordcloud(data, filename):
    """Creates a wordcloud for the given data.

    Preprocesses the data and creates a wordcloud for in that will be saved in
    the given filename."""
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logger = logging.getLogger('create_wordcloud')
    stopwords = read_utils.read_hotel_specific_stopwords(logger)

    tp = TextPreprocessor()
    preprocessed_entries = [tp.preprocess_text_for_wordcloud(X)
                            for X in data]
    tokens = [Y for X in preprocessed_entries for Y in X.split()]
    # Converts each token into lowercase
    for token in tokens:
        token = token.lower()

    comment_words = ''
    for words in tokens:
        comment_words = comment_words + words + ' '

    wordcloud = WordCloud(width=800,
                          height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(filename)
    # plt.show()


if __name__ == '__main__':
    data = ['house', 'house mouse', 'house mouse']
    filename = os.path.join(os.path.dirname(__file__), 'test_wordcloud_image')
    create_wordcloud(data, filename)
