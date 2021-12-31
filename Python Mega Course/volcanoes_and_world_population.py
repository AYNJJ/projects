import folium as fm
import pandas as pd

#volcanos location data from file
data = pd.read_csv("world-volcanoes.txt",sep=";",encoding = "ISO-8859-1")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

#color function based on elevation value
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'
#map base
m = fm.Map(location=[38.5, -99.09], zoom_start=5, tiles = None)
fm.TileLayer('cartodbpositron', name='World Map').add_to(m)

#add feature group for volcanoes, to add as child later
fgv = fm.FeatureGroup(name="Volcanoes")

#add circle markers for volcano locations based on above coordinates from file
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(fm.CircleMarker(location=[lt, ln], radius=6, popup=str(el)+ "m",
    fill_color=color_producer(el), color = 'grey', weight=1, fill_opacity=0.9))

#add feature group for volcanoes, to add as child later
fgp = fm.FeatureGroup(name="World Population")
#add world population data, below code colours countries based on range of population 10mil, between 10 and 20mil and over 20mil
fgp.add_child(fm.GeoJson(data=open('world.json', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

m.add_child(fgv)
m.add_child(fgp)
#add layer control below base map, it looks for all add_child objects and separates them in layers
m.add_child(fm.LayerControl())
m.save("volcanoes_and_world_population.html")
