import sys
from io import BytesIO

import requests
from PIL import Image

from commands import get_spn_from_envelope, get_coordinates

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

toponym_to_find = ' '.join(sys.argv[1:])

address_ll, envelope = get_coordinates(toponym_to_find)

search_params = {
    "apikey": api_key,
    'text':   toponym_to_find,
    "lang":   "ru_RU",
    "ll":     address_ll,
    "type":   "biz"
    }

response = requests.get(search_api_server, params=search_params)
if not response:
    exit(response)

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

spn = get_spn_from_envelope(envelope)

map_params = {
    "ll":  address_ll,
    "spn": spn,
    "l":   "map",
    "pt":  f"{org_point},pm2dgl"
    }

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
