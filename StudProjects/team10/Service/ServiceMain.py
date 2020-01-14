


# This service is responsible for the main calls fromm the gui
# it will contain the other services that will contain the bussiness
# methhods and will ddeal with the combining of methods
from Service.ServiceText import ServiceText
from Service.ServiceImage import ServiceImage
from Service.ServiceRoute import ServiceRoute
import datetime

class ServiceMain:


    # receives as parameteres the other services
    def __init__(self,servText: ServiceText, servImage: ServiceImage, servRoute: ServiceRoute):
        self.__servText=servText
        self.__servImage=servImage
        self.__servRoute=servRoute

    def __init__(self):
        self.__servText=ServiceText()
        self.__servImage=ServiceImage()
        self.__servRoute=ServiceRoute()

    # userText is the text received from the user as a string
    def getTextLocation(self,userText):
        listLocationByText=self.__servText.TextToTextAlgorithm(userText)
        listLocationByLabel= []
        # labelList=self.__servText.extractLabelsAlgorithm(userText)
        # print("label list: " , labelList)
        # listLocationByLabel=self.__servText.LabelToLabelComparison(labelList)
        listLocationsFinal=self.combineLocationList(listLocationByLabel,listLocationByText)
        return listLocationsFinal


    # Receives two lists
    # Each list's element is of form : ( label, probability )
    # label is a string, probability is a number between 0 and 1
    def combineLocationList(self, listLocationByLabel, listLocationByText):

        getTopText = listLocationByText[:4]
        # location_list_from_labels = [ loc[0] for loc in getTopLabels ]
        # objectives_list = []
        # for list in getTopText:
        #     location = list[2]
        #     if location in location_list_from_labels:
        #         objectives_list.append(list)
        return getTopText

    # imagePath is the path of a png image
    def getImageLocation(self,imagePath):
        labelList=self.__servImage.extractLabelsAlgorithm(imagePath)

        listLocationsFinal=self.__servText.LabelToLabelComparison(labelList)

        return listLocationsFinal


    # userText is the text received from the user as a string
    # imagePath is the path of a png image
    def getImageTextLocation(self,userText,imagePath):
        listImageLocation=self.getImageLocation(imagePath)
        listTextLocation=self.getTextLocation(userText)

        listLocationsFinal=self.combineLocationList(listImageLocation,listTextLocation)
        return listLocationsFinal



    # returns a list of Locations
    # location is a string
    # filters is a list of strings, each of them is a category of interest
    def getObjectivesByLocationAndFilter(self,location,filters):
        return self.__servRoute.getObjectivesByLocationAndFilter(location,filters)

    # returns a list of strings, each string is a category of interest
    def getFilters(self):
        return self.__servRoute.getFilters()

    # the param is a dictionary with the key being a Location and the value being the importance level
    # returns an image and an itinerary of the trip
    def getRouteByLocationsAndImportance(self,importanceLocationDictionary):


        # startTime=datetime.datetime.now().isoformat()
        print(importanceLocationDictionary)
        itinerary,tranz,image=self.__servRoute.getObjectivesVisitsRoute(importanceLocationDictionary)
        return itinerary,tranz,image

    def getRouteVisualization(self):
        self.__servRoute.getRouteVisualization()

# service = ServiceMain()
# service.getTextLocation("I wish to go with my family in a warm place where my children can go to the pool and where my husband can play poker. Also I want this place to be in the United States. Somewhere in California should do the trick. We would like to spend 10 thousand dollars and we want to go this summer.")
# service.getTextLocation("I wish to go with my family in a warm place where my children can go to the pool and where my husband can play poker. Also I want this place to be in Paris, near eiffel tower.")
# print(service.getTextLocation("My husband and I want to visit Europe in August. My husband wants to participate to an art european festival and I am a hill hiking lover."
#                         " We would enjoy visiting some museums too."))