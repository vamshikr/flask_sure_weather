import json
import logging
import os
from http import HTTPStatus

import requests

from flask_weather.exceptions import WeatherServiceException
from flask_weather.weather.base_service import BaseWeatherService


class WeatherDotCom(BaseWeatherService):
    """
    Weather.com service
    """
    SERVICE_NAME = 'weather.com'
    BASE_URL_KEY = 'WEATHERDOTCOM_URL'

    def __init__(self):
        super().__init__()
        self.url = os.environ[self.BASE_URL_KEY]

    def _get_current_weather(self, latitude: float, longitude: float):
        """
        For a given location gets the current weather report from weather.com
        :param latitude:
        :param longitude:
        :return:
        """
        data = {
            'lat': str(latitude),
            'lon': str(longitude)
        }

        response = requests.post(self.url + "/weatherdotcom", json=data)
        if response.status_code == HTTPStatus.OK:
            return json.loads(response.text)

    def get_current_temperature(self, latitude: float, longitude: float):
        """
        For a given location gets the current temperature in fahrenheit from weather.com
        :param latitude:
        :param longitude:
        :return:
        """
        try:
            report = self._get_current_weather(latitude, longitude)
            return float(report["query"]["results"]["channel"]["condition"]["temp"])
        except KeyError as err:
            logging.exception(err)
            raise WeatherServiceException from err
