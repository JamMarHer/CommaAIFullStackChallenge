import json

class DataProcessing(object):

    GEOJSON_LINE_SCHEMA_PATH = "geoJsonSchemas/pathSchema.json"

    """docstring for DataProcessing."""

    def __init__(self, path):
        super(DataProcessing, self).__init__()
        self.path = path

    def getGeoJsonOf(self, tripData):
        lineSchemaGeoJson = self.loadJson(self.GEOJSON_LINE_SCHEMA_PATH)
        listToAppend = []
        for positionMeta in tripData["coords"]:
            listToAppend.append([positionMeta["lng"], positionMeta["lat"]])
        lineSchemaGeoJson["features"][0]["geometry"]["coordinates"] = listToAppend
        return lineSchemaGeoJson

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
