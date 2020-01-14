import webbrowser

from imageRecogWatson.ImgEntityProbabilty import ImgObj
from imageRecogWatson.ImgRecognition import getFeatFromPicture


def openWeb(list_searchEntities):
    q = ""
    for i in range(len(list_searchEntities)):
        if i == len(list_searchEntities) - 1:
            q = q + list_searchEntities[i]
        else:
            q = q + list_searchEntities[i] + "%20"

    print("Q:", q)
    search_query = "https://www.tripadvisor.com/Search?singleSearchBox=true&pid=3826&redirect=&startTime=1572885936551" \
                   "&uiOrigin=MASTHEAD" \
                   "&q=" + q + "&supportedSearchTypes=find_near_stand_alone_query&enableNearPage=true&returnTo" \
                               "=__2F__ShowTopic__2D__g1__2D__i12105__2D__k3853337__2D__Search__5F__Reviews__5F__for__5F__specific__5F__words__2D__TripAdvisor__5F__Support__2E__html&searchSessionId=7CE6DCF9F5014C8AF73421C357458BCC1572885930902ssid&social_typeahead_2018_feature=true&sid=7CE6DCF9F5014C8AF73421C357458BCC1572888156643&blockRedirect=true&ssrc=h&geo=4&rf=1 "

    webbrowser.open(search_query)


def main():
    list_searchEntities = getFeatFromPicture('etr.jpg')
    print(list_searchEntities)

    final_results=[]
    list_entities=[]

    for obj in list_searchEntities:
        final_results.append(ImgObj(obj[0], obj[1]))
        list_entities.append(obj[0])
    #openWeb(list_entities)


#main()


def imgToLabel(src):
    list_searchEntities = getFeatFromPicture(src)

    print(list_searchEntities)

    final_results = []

    for obj in list_searchEntities:
        final_results.append(ImgObj(obj[0], obj[1]))

    for obj in final_results:#for debug
        print(obj)
    #print(final_results)

imgToLabel('etr.jpg')