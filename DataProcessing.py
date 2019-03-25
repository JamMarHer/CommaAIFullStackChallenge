import json
import math
from datetime import datetime
from os import listdir
from os.path import isfile, join
import pickle

class DataProcessing(object):

    GEOJSON_LINE_SCHEMA_PATH = "JsonSchemas/geoPathSchema.json"
    VEGA_GRAPH_SCHEMA_PATH = "JsonSchemas/graph.json"

    """docstring for DataProcessing."""

    def __init__(self, path):
        super(DataProcessing, self).__init__()
        self.path = path

    def getAllTripsData(self):
        allData = dict()
        listOfTrips = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        cachedData = self.loadData()
        if (cachedData):
            return cachedData
        for tripFile in listOfTrips:
            tripRawData = self.loadTripByName(tripFile)
            g, s, d, se= self.getColorLineParams(tripRawData)
            graphData = self.getTripGraph(location=g, speed=s, distance=d,
                                                                startEnd=se)

            allData[tripFile] = {
                "tripName": tripFile.split(".")[0],
                "location": g,
                "speed": s,
                "distance": d,
                "graph": graphData
                }
        self.saveData(allData)
        return allData

    def getTripGraph(self, location, speed, distance, startEnd):
        tripTime = self.getDifferenceInTime(startEnd) # In Minutes
        data = self.loadJson(self.VEGA_GRAPH_SCHEMA_PATH)
        values = []
        for minute in range(tripTime):
            if (minute * 60 < len(speed)):
                values.append({"time":minute, "speed":speed[minute *60]})
        data["data"][0]["values"] = values
        return data





    def getColorLineParams(self, tripData):
        lineSchemaGeoJson = self.loadJson(self.GEOJSON_LINE_SCHEMA_PATH)
        geoPositionsList = []
        distanceList = []
        speedList = []
        startEndTime = (tripData["start_time"], tripData["end_time"])

        for positionMeta in tripData["coords"]:
            geoPositionsList.append((positionMeta["lat"], positionMeta["lng"]))
            speedList.append(positionMeta["speed"])
            distanceList.append(positionMeta["dist"])
        #lineSchemaGeoJson["features"][0]["geometry"]["coordinates"] = listToAppend
        return geoPositionsList, speedList, distanceList, startEndTime

    def loadTripByName(self, fileName):
        fullPath = "{}/{}".format(self.path, fileName)
        jsonData = self.loadJson(fullPath)
        if (not jsonData):
            print("Incorrect file path or data type: \'{}\'".format(fullPath))
            exit(1)
        return jsonData

    # Returns time difference in minutes
    def getDifferenceInTime(self, startEndTime):
        format = '%Y-%m-%dT%H:%M:%S'
        start = datetime.strptime(startEndTime[0], format)
        end = datetime.strptime(startEndTime[1], format)

        timeDiff = end - start
        return int(round(timeDiff.total_seconds()/60))

    def loadJson(self, fullPath):
        with open(fullPath) as f:
            data = json.loads(f.read())
            return data
        return None

    def saveData(self, data):
        with open(".allData", 'wb') as fp:
            pickle.dump(data, fp)

    def loadData(self):
        try:
            with open (".allData", 'rb') as fp:
                data = pickle.load(fp)
                return data
        except Exception:
            return False
        return False
