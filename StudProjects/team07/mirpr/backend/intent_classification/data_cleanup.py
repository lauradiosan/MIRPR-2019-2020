import re
import ssl

import nltk
import pandas as pd
from keras_preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder


def load_data(filename):
    df = pd.read_csv(filename, names=["Sentence", "Intent"])
    intent = df["Intent"]
    unique_intent = list(set(intent))
    if " Intent" in unique_intent:
        unique_intent.remove(" Intent")
    sentences = list(df["Sentence"])
    sentences = sentences[1:]
    intent = intent.drop(intent.index[0])
    return intent, unique_intent, sentences


def cleaning(sentences):
    words = []
    for s in sentences:
        clean = re.sub(r'[^ a-z A-Z 0-9]', " ", s)
        w = word_tokenize(clean)
        # stemming
        words.append([i.lower() for i in w])

    return words


def create_tokenizer(words, filters = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'):
    token = Tokenizer(filters=filters)
    token.fit_on_texts(words)
    return token


def max_length(words):
    return len(max(words, key=len))


def encoding_doc(token, words):
    return token.texts_to_sequences(words)


def padding_doc(encoded_doc, max_length):
    return pad_sequences(encoded_doc, maxlen=max_length, padding="post")


def one_hot(encode):
    o = OneHotEncoder(sparse=False)
    return o.fit_transform(encode)


intent, unique_intent, sentences = load_data("input_files/vacation_intent_data.csv")
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


#tokenizer library needs this data
nltk.download("stopwords")
nltk.download("punkt")

cleaned_words = cleaning(sentences)
word_tokenizer = create_tokenizer(cleaned_words)
vocab_size = len(word_tokenizer.word_index) + 1
max_length_cleaned_words = max_length(cleaned_words)