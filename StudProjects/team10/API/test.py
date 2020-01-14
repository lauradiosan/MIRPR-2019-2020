from API.ItineraryAPI.TravelItinerary import *
import shutil

'''l = [Location("loc1", 46.779792, 23.620796),
     Location("loc2", 46.766435, 23.589105),
     Location("loc3", 46.775976, 23.603794)]'''
l = [Location.get_locations_by_query("iulius mall")[0],
     Location.get_locations_by_query("piata unirii cluj")[0],
     Location.get_locations_by_query("the office")[0]]
#start = Location("start", 46.774775, 23.621636)
start = Location.get_locations_by_query("economica 2")[0]
end = Location.get_locations_by_query("iulius mall")[0]
ti = TravelItinerary("2019-11-09T08:00:00", "2019-11-09T22:00:00", start, start)

ti.add_visit(l[0], "02:00:00", 1)
ti.add_visit(l[1], "01:00:00", 2)
ti.add_visit(l[2], "02:00:00", 3)

#visits, tranz = ti.compute_route()
visits, tranz, map = ti.compute_route_and_get_map()


print("Starting from: ")
print(start.name)
print(start.latitude)
print(start.longitude)

for i in range(len(visits)):
    print("\nTransition:")
    print(tranz[i])
    print("\nVisit: ")
    print(visits[i])

print("\nTransition:")
print(tranz[-1])

print("\nEnding at: ")
print(start.latitude)
print(start.longitude)


with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(map, out_file)

'''import wikipedia

# query = query.replace("Wikipedia", " ")
q = "Turda"
try:
    results = wikipedia.summary(q, sentences=4)
except Exception as e:
    print("This search may bring multiple results " + e)
print("According to wikipedia")
print(results)

import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "format": "json",
    "titles": "Turda",
    "prop": "coordinates"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
PAGES = DATA['query']['pages']

for k, v in PAGES.items():
    print("Latitute: " + str(v['coordinates'][0]['lat']))
    print("Longitude: " + str(v['coordinates'][0]['lon']))'''


