import webbrowser
import wikipedia

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
    print("Longitude: " + str(v['coordinates'][0]['lon']))