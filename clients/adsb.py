import requests
import json

url = "https://api.adsb.lol"

suffix = "/v2/mil"

response = requests.get(url + suffix, timeout=10)

response.raise_for_status()

data = response.json()



print(data.keys())