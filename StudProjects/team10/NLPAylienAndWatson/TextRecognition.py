import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions, KeywordsOptions, EntitiesOptions

from AylienDependency.ayilien import AYLIENClient
from NLPAylienAndWatson.EntityProb import EntityProb


def getFeatFromText(text):
    authenticator = IAMAuthenticator('WHorjeEwYYM9pazs9uDLsQbGpAooOIVyltsTlXOa_Rz4')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://gateway-lon.watsonplatform.net/natural-language-understanding/api')

    # response = natural_language_understanding.analyze(
    #     text=text,
    #     features=Features(keywords=KeywordsOptions(sentiment=True, emotion=True, limit=5))).get_result()

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            keywords=KeywordsOptions(emotion=True, sentiment=False,
                                     limit=6))).get_result()


    print(json.dumps(response, indent=2))

    jsonResponse = response['keywords']

    list_keywords = []

    for jso in jsonResponse:
        if jso['relevance'] > 0.5:
            list_keywords.append(EntityProb(jso['text'], jso['relevance']))

    print([obj.getEntity() for obj in list_keywords])

    return list_keywords

    #features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=5))).get_result()
    #print(json.dumps(response, indent=2))


def getLocationDateAndMoney(text):
    list_locations = []
    list_dates = []
    list_money = []

    text_api = AYLIENClient()

    responseEntities = text_api.get_tweet_entities(text)

    try:
        list_locations = responseEntities["entities"]["location"]
    except:
        print("No data for locations")

    try:
        list_dates = responseEntities["entities"]["date"]
    except:
        print("No data for date")
    try:
        list_money = responseEntities["entities"]["money"]
    except:
        print("No data for budget")

    return [list_locations, list_dates, list_money]



#getFeatFromText('I wish to go with my family in a warm place where my children can swim and where my husband can '
#                    'gamble. Also I want this place to be in the United States. Somewhere in California should do the '
#                    'trick. The budget is around 10 thousand dollars and we want to go this summer. ')
#print()
#print(getLocationDateAndMoney('I wish to go with my family in a warm place where my children can swim and where my husband can '
#                    'gamble. Also I want this place to be in the United States. Somewhere in California should do the '
#                    'trick. The budget is around 10 thousand dollars and we want to go this summer. '))
#print("Features:")
#print(l)
