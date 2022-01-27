import requests


def get_spn_from_envelope(envelope):
    l, b = envelope['lowerCorner'].split()
    r, t = envelope['upperCorner'].split()
    dx, dy = abs(float(l) - float(r)) / 2, abs(float(b) - float(t)) / 2
    return f'{dx},{dy}'


def get_coordinates(toponym):
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        "apikey":  "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym,
        "format":  "json"
        }

    response = requests.get(geocoder_api_server, params=geocoder_params).json()
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    envelope = toponym['boundedBy']['Envelope']

    return ','.join(
        response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
            'pos'].split()), envelope
