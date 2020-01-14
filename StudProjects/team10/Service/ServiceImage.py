from imageRecogWatson.ImgEntityProbabilty import ImgObj
from imageRecogWatson.ImgRecognition import getFeatFromPicture
class ServiceImage:
    def __init__(self):
        pass

    def extractLabelsAlgorithm(self,src):
        list_searchEntities = getFeatFromPicture(src)

        print(list_searchEntities)

        final_results = []

        for obj in list_searchEntities:
            final_results.append(ImgObj(obj[0], obj[1]))

        for obj in final_results:#for debug
            print(obj)

        return final_results
