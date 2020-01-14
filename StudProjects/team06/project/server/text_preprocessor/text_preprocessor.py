"""A class for preprocessing open text."""
import logging

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer  
  
from os.path import dirname

# from textblob import TextBlob

from word2number import w2n

import imp

from . import read_utils

class TextPreprocessor:   
    def __init__(self):
        logging.basicConfig(format='%(asctime)-15s %(message)s')
        self.__logger = logging.getLogger('TextPreprocessor')

        self.__stopwords = read_utils.read_stopwords(self.__logger)
        self.__punctuation = '[!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]:\''


    def preprocess_text(self, raw_text):
        """Preprocesses the given text and returns the result.
        
        Steps for preprocessing:
          - spelling correction
          - transforms the given raw text to lowercase
          - remove punctuation and stopwords"""
        # Spelling correction.
        # text_blob = TextBlob(raw_text)
        # raw_text = str(text_blob.correct())
        # Transform the given raw text to lowercase.
        tokens = word_tokenize(raw_text.lower())
        # Remove stopwords and punctuation.
        filtered_tokens = [T for T in tokens if self.__should_keep_token(T)]
        preprocessed_text = ' '.join(filtered_tokens)
        return preprocessed_text

      
    def preprocess_text_for_wordcloud(self, raw_text):
        """Preprocesses the given text and returns the result.
        
        Similar to preprocess_text method but removes numbers and lemmatizes
        the words."""
        preprocessed_text = preprocess_text(raw_text)
        tokens = word_tokenize(preprocessed_text)
        # Lematize tokens.
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(T) for T in tokens]
        # Remove numbers.
        tokens = [T for T in tokens if not self.__is_number(T)]
        preprocessed_text = ' '.join(tokens)
        return preprocessed_text


    def __is_number(self, text):
        # TODO: move this
        if text.isnumeric():
            return True
        try:
            w2n.word_to_num(text)
            return True
        except:
            return False


    def __should_keep_token(self, token):
      """Checks whether the given token should be kept.
      
      Returns false if the token is a punctuation sign or a stopword, otherwise
      returns true."""
      return token not in self.__punctuation and token not in self.__stopwords


if __name__ == '__main__':
    tp = TextPreprocessor()

    raw_text = 'I want to go to Paris, sometime this summer, together with my two kids.'
    preprocessed_text = tp.preprocess_text(raw_text)
    preprocessed_text_for_wordcloud = tp.preprocess_text_for_wordcloud(raw_text)
    print(raw_text)
    print(preprocessed_text)
    print(preprocessed_text_for_wordcloud)
