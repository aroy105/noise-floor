import requests
import json

url = "https://api.adsb.lol"


# aircraft near gdansk, 250 nautical miles
suffix = "/v2/lat/54.35/lon/18.65/dist/250"

response = requests.get(url + suffix, timeout=10)

response.raise_for_status()

data = response.json()
# keys = dict_keys(['ac', 'msg', 'now', 'total', 'ctime', 'ptime'])
# Existing aircraft in radius
print(data['total'])

# nic - Navigation Integrity Category
# reliability of reported aircraft position, based on containment radius. 
# Higher values -> smaller containment radius, better positional integrity
# nac_p - Navigation Accuracy Category for Position
# Accuracy of aircraft reported position, higher values -> more accurate

# if field is missing, nic or nac_p not available, so key is ommitted
# if value = 0, field is present, but integrity or accuracy is unknown/insufficient
filtered = [
    ac for ac in data["ac"]
    if ac.get("nic", 0) > 0
    and ac.get("nac_p", 0) > 0
]
print(len(filtered))
