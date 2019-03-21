import folium


class MapHandler(object):
    """docstring for MapHandler."""

    def __init__(self):
        super(MapHandler, self).__init__()

    def saveExampleMap(self):
        map = folium.Map(location=[37.74977073928103,-122.39242219446099], zoom_start=12)
        folium.Marker([37.74977073928103,-122.39242219446099],
                        popup='<strong>Start</strong>').add_to(map)
        folium.Marker([37.36531661007267,-122.40431714930452],
                        popup='<strong>Start</strong>').add_to(map)


        map.save('Map.html')
