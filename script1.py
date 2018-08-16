import folium
import pandas
'''
Use machine learning and the volcanoes data to create a data classification model that can guess with some probability what the hight of a volcano is given its location
'''


df = pandas.read_csv("Volcanoes_USA.txt")
df['NAME'] = df['NAME'].apply(lambda name: name.replace("'", ""))#this remove error from txt file, turns out there is a line creates and string error do to miss place quotation marks
map = folium.Map(location=[df['LAT'].mean(),df['LON'].mean()],zoom_start=4,tiles='Stamen Terrain')

def color(elev):
    minimum=int(min(df['ELEV']))
    step=int((max(df['ELEV'])-min(df['ELEV']))/3)
    if elev in range(minimum, minimum + step):
        col='green'
    elif elev in range(minimum + step, minimum + step*2):
        col='orange'
    else:
        col='red'
    return col

for lat, lon, name, elev in zip(df['LAT'],df['LON'],df['NAME'],df['ELEV']):
    map.add_child(folium.Marker(location=[lat,lon],popup=name,icon=folium.Icon(color=color(elev))))

map.add_child(folium.GeoJson(data=open('world_population.json', encoding = "utf-8-sig").read(),
name='world population',
style_function=lambda x: {'fillcolor' : 'green' if x['properties']['POP2005'] <= 10000000 else 'orange' if 10000000 < x ['properties']['POP2005'] < 20000000 else 'red'}))

map.save(outfile='test.html')
