from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

import re

from pandas.core.common import flatten

NUMBER_OF_KEYWORDS=10

def extract_keywords(data, stopwords, max_df=0.85):
    """TODO

    Args:
        data: list of strings.
    
    By default, ignore words that appear in 85% of entries. Eliminate stopwords.
    """
    # TODO: solve this
    if data == "No Negative":
        return []
        
    try:
        words = data.split()
        word_freqencies = [words.count(w) for w in words]
        word_freqencies = dict(list(zip(words, word_freqencies)))
        word_freqencies = [(word_freqencies[key], key) for key in word_freqencies]
        word_freqencies.sort()
        word_freqencies.reverse()
        words_frequencies = list(words_frequencies)[:NUMBER_OF_KEYWORDS]
        return words_frequencies
    except Exception as e:
        print("reviews_analyzer.keywords_utils.extract_keywords:", e)
        return []


def extract_keywords_old(data, stopwords, max_df=0.85):
    """TODO

    Args:
        data: list of strings.
    
    By default, ignore words that appear in 85% of entries. Eliminate stopwords.
    """
    # TODO: solve this
    if data == "No Negative":
        return []
        
    data = [data]
    data = flatten(data)
    try:
        cv = CountVectorizer(max_df=max_df,stop_words=stopwords)
        cv.fit(data)
        words_frequencies = sorted(cv.vocabulary_.items(), 
            key = lambda kv:(kv[1], kv[0]), reverse=True)
        words_frequencies = list(words_frequencies)[:NUMBER_OF_KEYWORDS]
        return words_frequencies
    except Exception as e:
        print("reviews_analyzer.keywords_utils.extract_keywords:", e)
        return []


def compute_tf_idf(data, stopwords):
    """TODO

    Args:
        data: a list of of list of strings, each list represents a cluster"""
    vectorizer = TfidfVectorizer(max_df=0.85,stop_words=stopwords)
    X = vectorizer.fit_transform(data)
    # print('=======================================')
    # print(vectorizer.get_feature_names())
    # print(vectorizer.vocabulary_)
    # print(vectorizer.idf_)
    # print(X)
    
    # cv = CountVectorizer(max_df=0.85,stop_words=stopwords)
    # word_count_vector = cv.fit_transform(data)

    # tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    # tfidf_transformer.fit(word_count_vector)
