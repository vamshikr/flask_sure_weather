import logging
from http import HTTPStatus

import requests


class GoogleMaps:

    HOST_NAME = 'maps.googleapis.com'
    HEADERS = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
    }

    def __init__(self, api_key):
        self.api_key = api_key

    def validate_location(self, latitude: float, longitude: float):

        params = {
            'latlng': '{},{}'.format(latitude, longitude),
            'key': self.api_key
        }

        response = requests.post('https://maps.googleapis.com/maps/api/geocode/json', params=params)
        if response.status_code == HTTPStatus.OK and response.json()['status'] == 'OK':
            return True

        return False

    def get_latlon(self, zipcode: int) -> tuple:

        params = {
            'address': zipcode,
            'key': self.api_key
        }

        response = requests.post('https://maps.googleapis.com/maps/api/geocode/json', params=params)
        if response.status_code == HTTPStatus.OK.value:
            data = response.json()
            logging.info(data)
            if data['results']:
                location = data["results"][0]["geometry"]["location"]
                return location["lat"], location["lng"]

        raise ValueError(f'Invalid zipcode: {zipcode}')
