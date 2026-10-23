import requests
import json

url = "https://api.adsb.lol"

# aircraft near gdansk, 250 nautical miles
suffix = "/v2/lat/54.35/lon/18.65/dist/250"


def adsbResponse(url, lat, lon, dist, timeout=10):
    personal_header = {
        "User-Agent": "noisefloor/0.1 aroy105"
    }
    return requests.get(f"{url}/v2/lat/{lat}/lon/{lon}/dist/{dist}", headers=personal_header, timeout=timeout)

response = adsbResponse(url, lat=54.35, lon=18.65, dist=250)

response.raise_for_status()

# keys = dict_keys(['ac', 'msg', 'now', 'total', 'ctime', 'ptime'])
data = response.json()

# nic - Navigation Integrity Category
# reliability of reported aircraft position, based on containment radius. 
# Higher values -> smaller containment radius, better positional integrity
# nac_p - Navigation Accuracy Category for Position
# Accuracy of aircraft reported position, higher values -> more accurate

# if field is missing, nic or nac_p not available, so key is ommitted
# if value = 0, field is present, but integrity or accuracy is unknown/insufficient

# Position can also be calculated by Multilateration (MLAT) rather than GPS, yielding missing nic and nac_p values
# Air Traffic Control (ATC) uses it by capturing Aircraft 1090 MHz signals, and ground receivers capture signal with time stamp,
# and a computer then triangulates the exact position. Immune to GNSS jamming

# so only filter for aircraft susceptible to GNSS jamming

jammable_aircraft_data = [ac for ac in data["ac"] if ac.get("type") != "mlat"]
total_jammable_aircraft = len(jammable_aircraft_data)
print(total_jammable_aircraft)

missing = [ac for ac in jammable_aircraft_data if "nic" not in ac or "nac_p" not in ac]
zeros = [ac for ac in jammable_aircraft_data if "nic" in ac and "nac_p" in ac and (ac.get("nic") == 0 or ac.get("nac_p") == 0)]
present = [
    ac for ac in jammable_aircraft_data
    if ac.get("nic", 0) > 0
    and ac.get("nac_p", 0) > 0
]

# count the buckets, confirm that we can account for every plane
print(len(missing), len(zeros), len(present), len(missing)+ len(zeros)+ len(present) == total_jammable_aircraft)
