import folium
import math

from DataProcessing import DataProcessing

class MapHandler(object):
    """docstring for MapHandler."""


    def __init__(self, tripsPath):
        super(MapHandler, self).__init__()
        self.dp = DataProcessing(tripsPath)

    def saveExampleMap(self):
        map = folium.Map(location=[37.74977073928103,-122.39242219446099], zoom_start=12, tiles = 'cartodbdark_matter')
        geo, speed, dist = self.dp.getColorLineParams(self.dp.loadTripByName("2016-07-02--11-56-24.json"))
        #folium.GeoJson(geoJsonData, name="2016-07-02--11-56-24").add_to(map)
        allOrderedData = self.dp.getAllTripsColorLineParams()

        for trip in allOrderedData:
            trip = allOrderedData[trip]
            tripColorLine = folium.features.ColorLine(
                trip["location"],
                colors = trip["speed"],
                colormap = ['r', 'orange', 'b'],
                weight = 3,
                name = trip["tripName"]
            )
            tripColorLine.add_to(map)
        map.save('Map.html')
