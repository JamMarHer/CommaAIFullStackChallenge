import folium
import math
import json
from DataProcessing import DataProcessing

class MapHandler(object):
    """docstring for MapHandler."""


    def __init__(self, tripsPath):
        super(MapHandler, self).__init__()
        self.dp = DataProcessing(tripsPath)

    def saveExampleMap(self):
        map = folium.Map(location=[37.74977073928103,-122.39242219446099], zoom_start=12, tiles = 'cartodbdark_matter')
        #geo, speed, dist, startEnd = self.dp.getColorLineParams(self.dp.loadTripByName("2016-07-02--11-56-24.json"))
        #folium.GeoJson(geoJsonData, name="2016-07-02--11-56-24").add_to(map)
        allOrderedData = self.dp.getAllTripsData()
        count = 0
        for trip in allOrderedData:
            count += 1
            trip = allOrderedData[trip]
            fg = folium.FeatureGroup(name=trip["tripName"])
            fg.add_child(folium.Popup(max_width=750).add_child(folium.Vega(trip["graph"],width=750, height=350)))
            tripColorLine = folium.features.ColorLine(
                trip["location"],
                colors = trip["speed"],
                colormap = ['r', 'orange', 'b'],
                weight = 1)

            fg.add_child(tripColorLine)
            map.add_child(fg)
            break


        map.save('Map.html')
