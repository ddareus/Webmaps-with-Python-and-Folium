import folium
import pandas

data = pandas.read_csv("volcanoes.txt")
lat = list(data.loc[:, 'LAT'])
lon = list(data.loc[:, 'LON'])
volname = list(data.loc[:, "NAME"])
volstatus = list(data.loc[:, 'STATUS'])
volelev = list(data.loc[:, "ELEV"])
vollocation = list(data.loc[:, 'LOCATION'])
voltype = list(data.loc[:, 'TYPE'])

html_popup = """<h4>Volcano information:</h4>
<p>Name: %s</p>
<p>Status: %s</p>
<p>Height: %s m</p>
<p>Location: %s </p>
<p>Type: %s </p>
"""


pythonmaps = folium.Map(location=[
                        18.918321222877136, - 73.51323138761227], zoom_start=9, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1001 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


for lt, ln, na, st, el, lc, tp in zip(lat, lon, volname, volstatus, volelev, vollocation, voltype):
    iframe = folium.IFrame(html=html_popup % (
        str(na), str(st), str(el), str(lc), str(tp)), width=200, height=100)
    fgv.add_child(folium.Marker(
        location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(el))))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(
    data=open('world.json', "r", encoding="utf-8-sig").read(),
    style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                              else 'orange' if 10000001 < x['properties']['POP2005'] < 100000000 else 'red'}))

pythonmaps.add_child(fgv)

pythonmaps.add_child(fgp)

pythonmaps.add_child(folium.LayerControl())

pythonmaps.save("Python_Webmaps.html")
