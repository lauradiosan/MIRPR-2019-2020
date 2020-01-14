import pathlib

import nltk

from NLPAylienAndWatson.TextRecognition import getFeatFromText, getLocationDateAndMoney
from NLPAylienAndWatson.TextObj import TextObj
from NLPAylienAndWatson.main import textToLabel
from Scrapping.textData import *
import pickle
#import Levenshtein
from nltk.corpus import wordnet

from TextSimilarity.text_sim_api import *


class ServiceText:
    def __init__(self):
        self.extension = ".txt"
        self.list_cities = ['Vienna', 'London', 'Lisbon', 'Berlin', 'Bucharest', 'Copenhagen', 'Edinburgh', 'Athens',
                       'Barcelona', 'Bern', 'St.Petersburg']

    def TextToTextAlgorithm(self, userText):
        return TextToText.get_top_similar_texts(userText)

    def extractLabelsAlgorithm(self, userText):
        # text = "I wish to go with my family in a warm place where my children can go to the pool and where my husband
        # can " \ "play poker. Also I want this place to be in Paris, near eiffel tower. Somewhere in California should
        # do the " \ "trick. We would like to spend 10 thousand dollars and we want to go this summer. "

        list_searchEntities = getFeatFromText(userText)
        result = getLocationDateAndMoney(userText)

        location = result[0]
        date = result[1]
        money = result[2]

        print("\n\n\nFinal Keywords:")
        # print(thisset)

        # print("Keywords:")
        # print(list_searchEntities)
        # print()

        locationStr = "-"
        dateStr = "-"
        moneyStr = "-"
        if location:
            # print("Location: ")
            # print(location[0])
            locationStr = location[0]
        if date:
            # print("Date: ")
            # print(date[0])
            dateStr = date[0]
        if money:
            # print("Budget: ")
            # print(money[0])
            moneyStr = money[0]

        objReturned = TextObj(list_searchEntities, locationStr, dateStr, moneyStr)
        # print(objReturned)

        labels_list = []
        for label in objReturned.getListOfObjectsWithProb():
            labels_list.append([label.getEntity(), label.getProb()])
        return labels_list

    def pushToFile(self, extension, list_objects, list_cities):
        for city in list_cities:
            with open(
                                    "C:\\Users\\ptido\\PycharmProjects\\MIRrepo\\planificator-vacanta-mirpr\\planificator-vacanta-mirpr\\Scrapping\\textData\\" + city + extension,
                                    'r', encoding="utf8") as content_file:
                content = content_file.read()
                # print(content)
                obj = textToLabel(content)
                list_objects.append(obj)

        with open('labelsFromWebTexts', 'wb') as f:
            pickle.dump(list_objects, f)

    def extractFromWebFiles(self, onParagraphs=False):
        extension = '.txt'
        list_objects = []
        list_cities = ['Vienna', 'London', 'Lisbon', 'Berlin', 'Bucharest', 'Copenhagen', 'Edinburgh', 'Athens',
                       'Barcelona', 'Bern', 'St.Petersburg']
        if not onParagraphs:
            self.pushToFile(extension, list_objects, list_cities)
        else:
            for city in list_cities:
                with open(city + extension, 'r', encoding="utf8") as content_file:
                    content = content_file.read()
                t = content.split(".")
                if len(t) > 8:
                    print(len(t))
                    texts = []
                    txt = ""
                    for i in range(len(t)):
                        txt = txt + t[i] + "."
                        if (i % 4 == 0 and i != 0) or i == len(t) - 1:
                            if i == len(t) - 1:
                                txt = txt[:-1]
                            texts.append(txt)
                            txt = ""

                    print(texts)
                    list_labelsForTextContent = []
                    for text in texts:
                        list_labelsForTextContent.append(textToLabel(text))

                    objT = TextObj([], '', '', '')
                    for obj in list_labelsForTextContent:
                        objT.setEntities(objT.getListOfObjectsWithProb() + obj.getListOfObjectsWithProb())
                        objT.setBudget(objT.getBudget() + obj.getBudget())
                        objT.setDate(objT.getDate() + obj.getDate())
                        objT.setLocation(objT.getLocation() + obj.getLocation())
                        list_objects.append(obj)

                else:
                    obj = textToLabel(content)
                    list_objects.append(obj)

            with open('labelsFromWebTexts', 'wb') as f:
                pickle.dump(list_objects, f)

    def getSavedLabelsFromFile(self):
        with open('labelsFromWebTexts', 'rb') as f:
            listTextObjs = pickle.load(f)
        list_cities = ['Vienna', 'London', 'Lisbon', 'Berlin', 'Bucharest', 'Copenhagen', 'Edinburgh', 'Athens',
                       'Barcelona', 'Bern', 'St.Petersburg']
        return [listTextObjs, list_cities]

    def LabelToLabelComparison(self, labelList):
        l = []
        for city in self.list_cities:
            labels = []

            similarity = 0
            goodPath = str(
                pathlib.Path(__file__).parent.parent.absolute()) + "\\Scrapping\\labels\\" + city + self.extension

            with open(goodPath.replace('\\','/'), 'rb') as f:
                obj = pickle.load(f)
                list_labels_for_cities = obj.getListOfObjectsWithProb()
                keywords = [x.getEntity() for x in list_labels_for_cities]
                keywords.append(city)
                print("labeltolable: " , keywords)

            for keyword in keywords:
                for label_prop in labelList:
                    label= label_prop[0]
                    if keyword =="Art Museum":
                        print("stop")
                    probability= label_prop[1]
                    keyword = keyword.lower()
                    label = label.lower()

                    if keyword == label:
                        if probability>=0.7:
                            similarity += 3
                        elif probability>=0.45:
                            similarity+=2
                        if keyword not in labels:
                            labels.append(keyword)

                    for word in keyword.split(" "):
                        #if Levenshtein.distance(word, label) < max(len(word), len(label))//2 and word not in labels:
                        if True:
                            if probability >= 0.7:
                                similarity += 2
                            elif probability >= 0.45:
                                similarity += 1
                            if word not in labels:
                                labels.append(word)
                            break
                        elif self.areSynonysm(label, word)and word not in labels:
                            if probability >= 0.7:
                                similarity += 2
                            elif probability >= 0.45:
                                similarity += 1
                            if word not in labels:
                                labels.append(word)
            l.append([city, similarity])


        l = sorted(l, key=lambda x: x[1], reverse=True)
        return l


    def areSynonysm(self, word1, word2):
        for synset in wordnet.synsets(word1):
            lemma = synset.lemma_names()
            if word2 in lemma:
                return True
        return False


# s = ServiceText()
# s.extractFromWebFiles()
#[listTextObjs, list_cities] = s.getSavedLabelsFromFile()
# print("-------------------------------")
# print(listTextObjs)
# print(listTextObjs[0])
# print(list_cities)
#
# list_cities = ['Vienna', 'London', 'Lisbon', 'Berlin', 'Bucharest', 'Copenhagen', 'Edinburgh', 'Athens',
#                'Barcelona', 'Bern', 'St.Petersburg']
#
# extension = ".txt"
#
# for i in range(0, len(list_cities)):
#     with open('0C:\\Users\\ptido\\PycharmProjects\\MIRrepo\\planificator-vacanta-mirpr\\planificator-vacanta-mirpr\\Scrapping\\labels\\' +
#                             list_cities[i] + extension, 'wb') as f:
#         pickle.dump(listTextObjs[i], f)
#print(s.get_word_synonyms_from_sent('happy', 'glad'))
# nltk.download()
#['Corinthia Lisbon', 'Sete Rios neighborhood of Lisbon', 'Portuguese capital.Corinthia Hotel Lisbon', 'Lisbon tour', 'bustling city center', 'good tourism office', 'Lisbon']

# print(s.LabelToLabelComparison(['Lisbon', 'neighbours', 'nice hotel', 'tourism', 'hostel', 'metropolis']))
