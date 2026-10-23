import requests
import json

base_url = "https://api.adsb.lol"

def adsb_response(url, lat, lon, dist, timeout=10):
    personal_header = {
        "User-Agent": "noisefloor/0.1 aroy105"
    }
    response = requests.get(f"{url}/v2/lat/{lat}/lon/{lon}/dist/{dist}", headers=personal_header, timeout=timeout)
    response.raise_for_status()
    # keys = dict_keys(['ac', 'msg', 'now', 'total', 'ctime', 'ptime'])
    return response.json()

# aircraft near gdansk, 250 nautical miles
data = adsb_response(base_url, lat=54.35, lon=18.65, dist=250)

# nic - Navigation Integrity Category
# reliability of reported aircraft position, based on containment radius. 
# Higher values -> smaller containment radius, better positional integrity
# nac_p - Navigation Accuracy Category for Position
# Accuracy of aircraft reported position, higher values -> more accurate
# note: NACp tends to drop first under jamming

# if field is missing, nic or nac_p not available, so key is ommitted
# if value = 0, field is present, but integrity or accuracy is unknown/insufficient

# Position can also be calculated by Multilateration (MLAT) rather than GPS, yielding missing nic and nac_p values
# Air Traffic Control (ATC) uses it by capturing Aircraft 1090 MHz signals, and ground receivers capture signal with time stamp,
# and a computer uses Time Difference of Arrival to get the exact position. Immune to GNSS jamming

# so only filter for aircraft susceptible to GNSS jamming. Focus just on adsb_icao right now
adsb_icao_aircraft_data = []
missing_nic, missing_nac_p, missing_nic_and_nac_p = [], [], []
zero_nic, zero_nac_p, zero_nic_and_nac_p = [], [], []
present = []

for ac in data["ac"]:
    if ac.get("type") == "adsb_icao":
        adsb_icao_aircraft_data.append(ac)
        if "nic" not in ac and "nac_p" not in ac:
            missing_nic_and_nac_p.append(ac)
        elif "nic" not in ac:
            missing_nic.append(ac)
        elif "nac_p" not in ac:
            missing_nac_p.append(ac)
        elif ac.get("nic") == 0 and ac.get("nac_p") == 0:
            zero_nic_and_nac_p.append(ac)
        elif ac.get("nic") == 0:
            zero_nic.append(ac)
        elif ac.get("nac_p") == 0:
            zero_nac_p.append(ac)
        else:
            present.append(ac)

total_adsb_icao_aircraft = len(adsb_icao_aircraft_data)

print(f"Total: {total_adsb_icao_aircraft}")
print(f"Missing NIC: {len(missing_nic)}")
print(f"Missing NAC_p: {len(missing_nac_p)}")
print(f"Missing NIC and NAC_p: {len(missing_nic_and_nac_p)}")
print(f"Zero NIC: {len(zero_nic)}")
print(f"Zero NAC_p: {len(zero_nac_p)}")
print(f"Zero NIC and NAC_p: {len(zero_nic_and_nac_p)}")
print(f"Present Aircraft: {len(present)}")

# Analyze the ones with Missing values
for ac in missing_nic:
    print(f"Lat: {ac["lat"]}, Lon: {ac["lon"]}, Alt_baro: {ac["alt_baro"]}, Version: {ac["version"]}, Flight: {ac["flight"]}")
for ac in missing_nac_p:
    print(f"Lat: {ac["lat"]}, Lon: {ac["lon"]}, Alt_baro: {ac["alt_baro"]}, Version: {ac["version"]}, Flight: {ac["flight"]}")
for ac in missing_nic_and_nac_p:
    print(f"Lat: {ac["lat"]}, Lon: {ac["lon"]}, Alt_baro: {ac["alt_baro"]}, Version: {ac["version"]}, Flight: {ac["flight"]}")
for ac in zero_nic:
    print(f"Lat: {ac["lat"]}, Lon: {ac["lon"]}, Alt_baro: {ac["alt_baro"]}, Version: {ac["version"]}, Flight: {ac["flight"]}")
for ac in zero_nac_p:
    print(f"Lat: {ac["lat"]}, Lon: {ac["lon"]}, Alt_baro: {ac["alt_baro"]}, Version: {ac["version"]}, Flight: {ac["flight"]}")
for ac in zero_nic_and_nac_p:
    print(f"Lat: {ac["lat"]}, Lon: {ac["lon"]}, Alt_baro: {ac["alt_baro"]}, Version: {ac["version"]}, Flight: {ac["flight"]}")

# Analyze the ones with Zero values