from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os.path import dirname

import logging
# import colorsys
# import random
import imp
import pandas
import numpy

from copy import deepcopy

import matplotlib.pyplot as plt
# from matplotlib.mlab import PCA as mlabPCA

from sklearn.cluster import KMeans, DBSCAN
# from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.metrics import silhouette_score

from yellowbrick.cluster import KElbowVisualizer

import tensorflow as tf
import tensorflow_hub as hub

from . import utils, io_utils, clustering_utils, keywords_utils
from .clustering_methond_type import ClusteringMethodType

from text_preprocessor import text_preprocessor, wordcloud_utils
from text_preprocessor.read_utils import read_stopwords, read_kewyords_stopwords

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ["TFHUB_CACHE_DIR"] = '/tmp/tfhub'


class ReviewsAnalyzer():
    def __init__(self,
                 data,
                 key_column,
                 columns_containing_text_to_analyse,
                 data_was_preprocessed=False):
        """TODO
        
        Args:
            data: pandas.DataFrame"""
        logging.basicConfig(format='%(asctime)-15s %(message)s')
        self.__logger = logging.getLogger('TextPreprocessor')

        self.__data = data
        self.__key_column = key_column
        self.__columns_containing_text_to_analyse = \
            columns_containing_text_to_analyse

        # Extract keys
        self.__keys = self.__data[self.__key_column]
        # Remove duplicates.
        self.__keys = list(dict.fromkeys(self.__keys))

        self.__data_was_preprocessed = data_was_preprocessed
        self.__data_was_encoded = False
        self.__data_was_clustered = False
        self.__sentiment_was_calculated = False
        self.__keywords_stopwords = read_kewyords_stopwords()


    def get_data(self):
        return self.__data


    def get_keys(self):
        return self.__keys


    def get_clusters(self, key, column):
        if not self.__data_was_preprocessed:
            return Exception('Data was not clustered.')
        if not key in self.__keys:
            return Exception('Invalid key.')
        if not column in self.__columns_containing_text_to_analyse:
            return Exception('Invalid column.')

        # Exchange each entry's label, which is an index, with its corresponding
        # entry in the given data table.
        results = deepcopy(self.__cluster_results[key][column])
        # Remove all data like "nothing", "no negative", "no positive"
        # etc. (all reviews that have no keywords) before clustering
        # as these reviews have no value for this part of the analysis.
        data_for_column = [X[column] for _, X in self.__data.iterrows() \
                           if X[self.__key_column] == key and \
                           keywords_utils.extract_keywords(X[column], 
                                                           self.__keywords_stopwords,
                                                           max_df=1)]
        for cluster in results:
            for entry in cluster.entries:
                value_for_label = data_for_column[entry.label]
                entry.label = value_for_label
        return results


    def get_sentiment(self, key, column):
        if not self.__sentiment_was_calculated:
            return Exception('Sentiment was not calculated.')

        sentiment_column_name = '_'.join([column, 'Sentiment'])
        entries = [(X) for _, X in self.__data.iterrows() \
                   if X[self.__key_column] == key]
        data_for_column = [X[sentiment_column_name] for X in entries]
        if not len(data_for_column):
            return 0

        overall_sentiment = 0
        for entry in data_for_column:
            overall_sentiment += entry
        overall_sentiment /= len(data_for_column)
        return overall_sentiment 


    def analyse(self, output_directory, method=ClusteringMethodType.KMEANS):
        self.preprocess_data()
        self.calculate_sentiment()
        self.encode_data()
        self.cluster_data(method)
        self.extract_keywords()
        self.create_word_clouds(output_directory)
        

    def preprocess_data(self):
        """Preprocess the raw data.

        For each entry (review), for each column of
        columns_containing_text_to_analyse, another column will be added....

        TODO: description"""
        if self.__data_was_preprocessed:
            raise Exception("Data was already preprocessed.")

        tp = text_preprocessor.TextPreprocessor()
        for column in self.__columns_containing_text_to_analyse:
            new_column_name = '_'.join([column, 'Preprocessed'])
            new_column_values = []

            for index, entry in self.__data.iterrows():
                raw_text = entry[column]
                
                # TODO: now it preprocesses only the first sentence, change this
                # The reviews are a bit processed aka no more punctuation =>
                # split text into sentences based on uppercase letters
                # raw_text = self.__extract_first_sentence(raw_text)

                preprocessed_text = tp.preprocess_text(raw_text)
                new_column_values = new_column_values + [preprocessed_text]

            self.__data[new_column_name] = new_column_values
        
        self.__data_was_preprocessed = True


    def calculate_sentiment(self):
        if self.__sentiment_was_calculated:
            return Exception('Sentiment was already calculated.')

        for column in self.__columns_containing_text_to_analyse:
            sentiment_column_name = '_'.join([column, 'Sentiment'])
            data_for_column = self.__data[column]
            sentiment = utils.calculate_sentiment_for_array(data_for_column)
            self.__data[sentiment_column_name] = sentiment
        
        self.__sentiment_was_calculated = True


    def encode_data(self):
        if not self.__data_was_preprocessed:
            return Exception('Data was not preprocessed.')
        if self.__data_was_encoded:
            raise Exception("Data was already encoded.")

        for column in self.__columns_containing_text_to_analyse:
            preprocessed_column_name = '_'.join([column, 'Preprocessed'])
            encoded_column_name = '_'.join([column, 'Encoded'])
            data_to_encode = self.__data[preprocessed_column_name]
            encoded_data = utils.encode(data_to_encode)
            self.__data[encoded_column_name] = encoded_data
        
        self.__data_was_encoded = True


    def cluster_data(self, method=ClusteringMethodType.KMEANS):
        """Clusters the data using the given method.""" 
        if not self.__data_was_encoded:
            return Exception('Data was not encoded.')

        self.__cluster_results = {}
        for key in self.__keys:
            self.__cluster_results[key] = {}
            entries = [(X) for _, X in self.__data.iterrows() \
                       if X[self.__key_column] == key]
            for column in self.__columns_containing_text_to_analyse:
                encoded_column_name = '_'.join([column, 'Encoded'])
                # Remove all data like "nothing", "no negative", "no positive"
                # etc. (all reviews that have no keywords) before clustering
                # as these reviews have no value for this part of the analysis.
                points = [X[encoded_column_name] for X in entries \
                          if keywords_utils.extract_keywords(X[column], 
                                                             self.__keywords_stopwords,
                                                             max_df=1)]
                points = ([numpy.array(X) for X in points])
                points = numpy.array(points)
                points = points.tolist()
                print(len(points))

                clusters = clustering_utils.cluster_data(points, method)
                self.__cluster_results[key][column] = clusters

                # kmeans = KMeans(n_clusters=5, random_state=0)
                # kmeans.fit(points)
                # y_kmeans = kmeans.fit_predict(points)

                # print(silhouette_score(points, kmeans.labels_))
                # continue

                # sc = SpectralClustering(3, 
                #                         affinity='precomputed', 
                #                         n_init=100,
                #                         assign_labels='discretize')

                # db = DBSCAN(eps=0.3, min_samples=10).fit(points)
                # core_samples_mask = numpy.zeros_like(db.labels_, dtype=bool)
                # core_samples_mask[db.core_sample_indices_] = True
                # labels = db.labels_

                # # Number of clusters in labels, ignoring noise if present.
                # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
                # n_noise_ = list(labels).count(-1)

                # print('Estimated number of clusters: %d' % n_clusters_)
                # print('Estimated number of noise points: %d' % n_noise_)
                # print("Silhouette Coefficient: %0.3f"
                #     % metrics.silhouette_score(points, labels))

                # continue

                # visualizer = KElbowVisualizer(kmeans, k=(5,15), metric='silhouette', timings=False)
                # visualizer.fit(points)    
                # visualizer.poof() 

        self.__data_was_clustered = True


    def extract_keywords(self):
        if not self.__data_was_preprocessed:
            return Exception('Data was not clustered.')

        for key in self.__keys:
            entries = [(X) for _, X in self.__data.iterrows() \
                       if X[self.__key_column] == key]
            for column in self.__columns_containing_text_to_analyse:
                preprocessed_column_name = '_'.join([column, 'Preprocessed'])

                for cluster in self.__cluster_results[key][column]:
                    indexes = [X.label for X in cluster.entries]
                    # Use the preprocessed reviews.
                    reviews = [entries[index][preprocessed_column_name] 
                        for index in range(len(entries))
                        if index in indexes]
                    cluster.keywords = \
                        keywords_utils.extract_keywords(reviews, self.__keywords_stopwords)


    def create_word_clouds(self, output_directory):
        """Creates wordclouds and save them in the given directory."""
        wordclouds_output_directory = \
            os.path.join(output_directory, 'wordclouds')
        
        for key in self.__keys:
            entries = [(X) for _, X in self.__data.iterrows() \
                       if X[self.__key_column] == key]
            for column in self.__columns_containing_text_to_analyse:
                entries_for_column = [X[column] for X in entries]
                # Save the wordcloud as an image to wordcloud_output_directory 
                # The filename contains the table key together with the column
                filename = '_'.join(key.split()) + '__' + '_'.join(column.split())
                output_path = os.path.join(wordclouds_output_directory, filename)
                wordcloud_utils.create_wordcloud(entries_for_column, output_path)


    def __split_reviews_in_sentences(self):
        number_of_initial_rows = len(self.__data)
        # TODO: second, third and so on are duplicated. solve this.
        for column in self.__columns_containing_text_to_analyse:
            for index in range(number_of_initial_rows):
                raw_text = self.__data.iloc[index][column]
                # If there are multiple sentences in a review, split the review
                # and update the table such that each review will contain only
                # one sentence.
                sentences = self.__extract_sentences(raw_text)
                
                # Only one sentence => no need to divide this row
                if len(sentences) == 1:
                    continue

                self.__data.iloc[index][column] = sentences[0]
                for i in range(1, len(sentences)):
                    new_row = self.__data.iloc[index]
                    new_row[column] = sentences[i]
                    self.__data = self.__data.append(new_row)


    def __extract_sentences(self, text):
        words = text.split()
        if not words:
            return ['nothing']
        
        sentences = []
        text = [words[0]]
        words = words[1:]
        exception_upper_words = ['I', 'TV', 'Tv', 'Euro', 'English', 'Ok', ' OK']
        for word in words:
            if word not in exception_upper_words and word[0].isupper():
                text = " ".join(text)
                sentences = sentences + [text]
                text = [word]
                continue
            text = text + [word]

        # Add last sentence
        text = " ".join(text)
        sentences = sentences + [text]
        return sentences
    

    def __extract_first_sentence(self, text):
        return self.__extract_sentences(text)[0]
