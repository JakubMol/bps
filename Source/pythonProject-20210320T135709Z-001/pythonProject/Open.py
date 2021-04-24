import requests
import json


def get(coordinates):
    data = tojson(coordinates)
    url = "https://api.open-elevation.com/api/v1/lookup"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.content
    else:
        raise ConnectionError(f"Status code: {response.status_code}")
    return request


def tojson(coordinates):
    return json.dumps({"locations": coordinates})


def todict(coordinates):
    return json.loads(get(coordinates))["results"]
