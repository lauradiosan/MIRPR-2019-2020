import csv
from os import walk

import paralleldots

class TextToText:
    count = 0
    api_keys = []

    @staticmethod
    def get_similarity(text1, text2):
        return paralleldots.similarity(text1, text2)

    @staticmethod
    def get_top_similar_texts( user_query):
        """
        :return: Returns a list of triplets, where every triplet consists of :
                    1. the entire text which was used in finding the similarity with the user's text
                    2. the similarity between the text from file and user's input
                    3. the name of the location
        """

        paralleldots.set_api_key(TextToText.api_keys[TextToText.count])
        TextToText.count+=1
        if TextToText.count == len(TextToText.api_keys):
            TextToText.count += 0

        sim_list = []
        list_cities = ['Vienna', 'London', 'Lisbon', 'Berlin', 'Bucharest', 'Copenhagen', 'Edinburgh', 'Athens',
                            'Barcelona', 'Bern', 'St.Petersburg']
        for city in list_cities:
            with open(r"../Scrapping/textData/" + city+".txt", encoding="utf8") as file:
                for line  in file.readlines()[:5]:
                    similarity = TextToText.get_similarity(text1=user_query, text2=line)
                    try:
                        sim_list.append([line, similarity["similarity_score"], city])
                    except:
                        print("error")
        sim_list= sorted(sim_list, key= lambda x : x[1], reverse=True)
        return sim_list

if __name__=="__main__":
    TextToText.get_top_similar_texts("I wish to go with my family in a warm place where my children can go to the pool and where my husband can play poker. Also I want this place to be in the United States. Somewhere in California should do the trick. We would like to spend 10 thousand dollars and we want to go this summer.")
    # get_top_similar_texts("I want to plan a surprise trip for me and my family. My husband is a hiking lover and my children adore long walks in the forest. "
    #                       "I want to go in a new place like Califoria to see giant sequoia trees for the first time. There is no budget limit. ")