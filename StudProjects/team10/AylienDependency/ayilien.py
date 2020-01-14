import webbrowser

from aylienapiclient import textapi
import csv
# from bs4 import BeautifulSoup

# c = textapi.Client("e14bf0bb", "bb2b6dbbfd5f6714ecbf6fca6141dd92")
# s = c.Sentiment({'text': 'John is a very good football player!'})
# print("S: ", s)


class AYLIENClient(object):
    # Generic AYLIEN Class for getting sentiment of of given text .

    def __init__(self):
        """
        Class constructor for authentication of Text api for AYLIEN  .
        """

        ## AYLIEN credentials
        application_id = "e14bf0bb"
        application_key = "bb2b6dbbfd5f6714ecbf6fca6141dd92"

        try:
            self.api = textapi.Client(application_id, application_key)
        except:
            print("Error: AYLIEN Authentication Failed")

    def get_tweet_sentiment(self, tweet):
        # function to classify sentiment of tweet
        response = self.api.Summarize(
            {'text': tweet, 'title': 'vacation', 'sentences_number': 1})  # self.api.Sentiment({'text': tweet})
        return response

    def get_tweet_entities(self, tweet):
        # function to classify sentiment of tweet
        response = self.api.Entities({'text': tweet})  # self.api.Sentiment({'text': tweet})
        print(response)
        return response

    def get_tweet_Concept(self, tweet):
        # function to classify sentiment of tweet
        response = self.api.Concepts({'text': tweet})  # self.api.Sentiment({'text': tweet})
        return response

    def get_tweet_EntityLevelAnalysis(self, tweet):
        # function to classify sentiment of tweet
        response = self.api.Elsa({'text': tweet})  # self.api.Sentiment({'text': tweet})
        return response

    def get_tweet_HashTags(self, tweet):
        # function to classify sentiment of tweet
        response = self.api.Hashtags({'text': tweet})  # self.api.Sentiment({'text': tweet})
        return response


#text_api = AYLIENClient()

# # query = 'John is a very good football player!'
# query = 'I wish to go with my family in a warm place where my children can go to the pool and where my husband can play poker. Also I want this place to be in the United States. Somewhere in California should do the trick. We would like to spend 10 thousand dollars and we want to go this summer.'
#
#
# 'https://www.tripadvisor.com/Search?singleSearchBox=true&geo=1&searchNearby=&pid=3826&redirect=&startTime=1575150818348&uiOrigin=MASTHEAD&q=chalet&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo=__2F__&searchSessionId=D180AF876856AFA7AB817DFF417058F41575150808534ssid&social_typeahead_2018_feature=true&sid=D180AF876856AFA7AB817DFF417058F41575150824644&blockRedirect=true&ssrc=h&rf=1'
# # query = 'Where is Bucharest'
# file_name = 'Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(1, query)

# response = text_api.get_tweet_sentiment(query)
#
# responseEntities = text_api.get_tweet_entities(query)
#
# responseConcepts = text_api.get_tweet_Concept(query)
#
# responseElsa = text_api.get_tweet_EntityLevelAnalysis(query)
#
# responseHashTags = text_api.get_tweet_HashTags(query)
#
# print("Response Smm: ", response["sentences"])
#
# print("Response Entities: ", responseEntities["entities"])
#
# print("Response Entities: ", responseConcepts["concepts"])
#
# print("Response Elsa: ", responseElsa["entities"])
#
# print("Response HashTag: ", responseHashTags["hashtags"])
#
# list_locations = responseEntities["entities"]["location"]
# list_tags = responseEntities["entities"]["keyword"]
# list_searchEntities = []
# for i in range(0, len(list_tags)):
#     if str(list_tags[i])[0].isupper() and list_tags[i] not in list_locations and str(list_tags[i]) != "United" and str(
#             list_tags[i]) != "States":
#         list_searchEntities.append(list_tags[i])
#
# list_searchEntities.append(list_tags[len(list_tags) - 1])
# list_searchEntities.append(list_tags[len(list_tags) - 2])
#
# q = ""
# for i in range(len(list_searchEntities)):
#     if i == len(list_searchEntities) - 1:
#         q = q + list_searchEntities[i]
#     else:
#         q = q + list_searchEntities[i] + "%20"
#
# print("Q:", q)
# search_query = "https://www.tripadvisor.com/Search?singleSearchBox=true&pid=3826&redirect=&startTime=1572885936551" \
#                "&uiOrigin=MASTHEAD" \
#                "&q=" + q + "&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo" \
#                            "=__2F__ShowTopic__2D__g1__2D__i12105__2D__k3853337__2D__Search__5F__Reviews__5F__for__5F__specific__5F__words__2D__TripAdvisor__5F__Support__2E__html&searchSessionId=7CE6DCF9F5014C8AF73421C357458BCC1572885930902ssid&social_typeahead_2018_feature=true&sid=7CE6DCF9F5014C8AF73421C357458BCC1572888156643&blockRedirect=true&ssrc=h&geo=4&rf=1 "

#webbrowser.open(search_query)
# with open(file_name, 'w', newline='') as csvfile:
#     csv_writer = csv.DictWriter(
#         f=csvfile,
#         fieldnames=["Tweet", "Sentiment"]
#     )
#     csv_writer.writeheader()
#
#     response = text_api.get_tweet_sentiment(query)
#     print("Response: ", response)
#
# print("Saved data in Sentiment_Analysis_of_{}_Tweets_About_{}.csv \n".format(1, query))

# query = "something easy something I don't have to worry about what can you offer"
# text_api = AYLIENClient()
# responseEntities = text_api.get_tweet_entities(query)
# responseHashTags = text_api.get_tweet_HashTags(query)
# print(responseEntities)
# print(responseHashTags)
# list_locations = responseEntities["entities"]["location"]

'''

"https://www.tripadvisor.com/Search?singleSearchBox=true&pid=3826&redirect=&startTime=1572885936551&uiOrigin=MASTHEAD" \
"&q=gamble%20warm&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo" \
"=__2F__ShowTopic__2D__g1__2D__i12105__2D__k3853337__2D__Search__5F__Reviews__5F__for__5F__specific__5F__words__2D__TripAdvisor__5F__Support__2E__html&searchSessionId=7CE6DCF9F5014C8AF73421C357458BCC1572885930902ssid&social_typeahead_2018_feature=true&sid=7CE6DCF9F5014C8AF73421C357458BCC1572888156643&blockRedirect=true&ssrc=h&geo=4&rf=1 "

"https://www.tripadvisor.com/Search?singleSearchBox=true&pid=3826&redirect=&startTime=1572885936551&uiOrigin=MASTHEAD" \
"&q=beach&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo" \
"=__2F__ShowTopic__2D__g1__2D__i12105__2D__k3853337__2D__Search__5F__Reviews__5F__for__5F__specific__5F__words__2D__TripAdvisor__5F__Support__2E__html&searchSessionId=7CE6DCF9F5014C8AF73421C357458BCC1572885930902ssid&social_typeahead_2018_feature=true&sid=7CE6DCF9F5014C8AF73421C357458BCC1572888046096&blockRedirect=true&ssrc=h&geo=4&rf=1 "

"https://www.tripadvisor.com/Search?singleSearchBox=true&pid=3826&redirect=&startTime=1572885936551&uiOrigin=MASTHEAD" \
"&q=gamble%20warm%20volcano&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo" \
"=__2F__ShowTopic__2D__g1__2D__i12105__2D__k3853337__2D__Search__5F__Reviews__5F__for__5F__specific__5F__words__2D__TripAdvisor__5F__Support__2E__html&searchSessionId=7CE6DCF9F5014C8AF73421C357458BCC1572885930902ssid&social_typeahead_2018_feature=true&sid=7CE6DCF9F5014C8AF73421C357458BCC1572888283077&blockRedirect=true&ssrc=h&geo=4&queryParsed=true "
'''
