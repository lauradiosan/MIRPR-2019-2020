import webbrowser

from NLPAylienAndWatson.TextObj import TextObj
from NLPAylienAndWatson.TextRecognition import getFeatFromText, getLocationDateAndMoney


def textToLabel(text):
    # text = "I wish to go with my family in a warm place where my children can go to the pool and where my husband
    # can " \ "play poker. Also I want this place to be in Paris, near eiffel tower. Somewhere in California should
    # do the " \ "trick. We would like to spend 10 thousand dollars and we want to go this summer. "

    list_searchEntities = getFeatFromText(text)
    # thisset = {'apple'}
    #
    # q = ""
    # texts = text.split(".")
    # print(texts)
    # for txt in texts:
    #     if txt:
    #         list_searchEntities = getFeatFromText(txt)
    #         print("Keywords:")
    #         print(list_searchEntities)
    #         for el in list_searchEntities:
    #             thisset.add(el)

    result = getLocationDateAndMoney(text)

    location = result[0]
    date = result[1]
    money = result[2]

    print()
    print()
    print()

    print("Final Keywords:")
    #print(thisset)

    print("Keywords:")
    print(list_searchEntities)
    print()

    q = ""

    locationString = ""
    dateString = ""
    moneyString = ""

    if location:
        print("Location: ")
        print(location[0])
        locationString = location[0]
    if date:
        print("Date: ")
        print(date[0])
        dateString = date[0]
    if money:
        print("Budget: ")
        print(money[0])
        moneyString = money[0]

    objReturned = TextObj(list_searchEntities, locationString, dateString, moneyString)
    print(objReturned)
    return objReturned
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
    #
    # webbrowser.open(search_query)

text = "I wish to go with my family in a warm place where my children can go to the pool and where my husband can " \
           "play poker. Also I want this place to be in Paris, near eiffel tower. Somewhere in California should do the " \
           "trick. We would like to spend 10 thousand dollars and we want to go this summer. "

#textToLabel(text)
