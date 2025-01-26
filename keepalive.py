import requests
import json

with open("secrets.json", "r") as f:
    url = json.load(f)['url']

print(requests.get(f"{url}/api/keepalive").text)
