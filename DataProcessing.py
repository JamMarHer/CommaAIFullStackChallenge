import json
from os import listdir
from os.path import isfile, join

class DataProcessing(object):

    GEOJSON_LINE_SCHEMA_PATH = "geoJsonSchemas/pathSchema.json"

    """docstring for DataProcessing."""

    def __init__(self, path):
        super(DataProcessing, self).__init__()
        self.path = path

    def getAllTripsColorLineParams(self):
        allData = dict()
        listOfTrips = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        for tripFile in listOfTrips:
            g, s, d = self.getColorLineParams(self.loadTripByName(tripFile))
            allData[tripFile] = {
                "tripName": tripFile.split(".")[0],
                "location": g,
                "speed": s,
                "distance": d
                }
        return allData



    def getColorLineParams(self, tripData):
        lineSchemaGeoJson = self.loadJson(self.GEOJSON_LINE_SCHEMA_PATH)
        geoPositionsList = []
        speedList = []
        distanceList = []
        for positionMeta in tripData["coords"]:
            geoPositionsList.append((positionMeta["lat"], positionMeta["lng"]))
            speedList.append(positionMeta["speed"])
            distanceList.append(positionMeta["dist"])
        #lineSchemaGeoJson["features"][0]["geometry"]["coordinates"] = listToAppend
        return geoPositionsList, speedList, distanceList

    def loadTripByName(self, fileName):
        fullPath = "{}/{}".format(self.path, fileName)
        jsonData = self.loadJson(fullPath)
        if (not jsonData):
            print("Incorrect file path or data type: \'{}\'".format(fullPath))
            exit(1)
        return jsonData


    def loadJson(self, fullPath):
        with open(fullPath) as f:
            data = json.loads(f.read())
            return data
        return None
