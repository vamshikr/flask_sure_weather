import json
import statistics
from datetime import datetime
import logging


from .exceptions import InputValidationException, WeatherServiceException, ServiceNotAvailable, \
    SureWeatherException, AppErrorCodes

@api.route('/current_weather')
class CurrentWeather(Resource):
    LATITUDE_KEY = 'latitude'
    LONGITUDE_KEY = 'longitude'
    SERVICES_KEY = 'services'
    ZIPCODE = 'zipcode'

    """
    Main class that handles the router /current_weather
    """

    def get_latlon(self, zipcode: str):
        """
        Uses google maps to get latitude and longitude from a given zipcode
        :param zipcode:
        :return: tuple (latitude, longitude)
        """
        if 'google_maps' not in self.request.app:
            raise ServiceNotAvailable(AppErrorCodes.SERVICE_NOT_AVAILABLE,
                                      'Google maps service not setup')

        return self.request.app['google_maps'].get_latlon(int(zipcode))

    def parse_request(self, query_params: dict) -> tuple:
        """
        Parses the request and returns a tuple of (latitude, longitude, services)
        This method groups the errors if it encounters any
        :param query_params:
        :return: tuple of (latitude, longitude, services)
        """
        errors = []
        latitude, longitude = None, None

        if self.ZIPCODE in query_params:
            try:
                latitude, longitude = self.get_latlon(query_params[self.ZIPCODE])
            except ValueError:
                errors.append('Invalid zipcode {}'.format(query_params[self.ZIPCODE]))

        elif self.LATITUDE_KEY in query_params and self.LATITUDE_KEY in query_params:

            logging.info(query_params)
            try:
                latitude = float(query_params[self.LATITUDE_KEY])

                if not -90 <= latitude <= 90:
                    errors.append(
                        'latitude invalid, must be decimal point number between -90 and +90')

            except ValueError:
                errors.append('latitude invalid, must be decimal point number between -90 and +90')

            try:
                longitude = float(query_params[self.LONGITUDE_KEY])

                if not -180 <= longitude <= 180:
                    errors.append(
                        'longitude invalid, must be decimal point number between -180 and +180')

            except ValueError:
                errors.append(
                    'longitude invalid, must be decimal point number between -180 and +180')

            if 'google_maps' in self.request.app and not \
                    self.request.app['google_maps'].validate_location(latitude,
                                                                            longitude):
                errors.append('This location is invalid')

        else:
            errors.append('[latitude, longitude] pair or zipcode must be present')

        if self.SERVICES_KEY in query_params:
            services = query_params[self.SERVICES_KEY].split(',')
            invalid_services = set(services).difference(self.request.app['weather_services'].keys())
            if invalid_services:
                errors.append('Invalid services {}'.format(invalid_services))
        else:
            services = list(self.request.app['weather_services'].keys())

        if errors:
            logging.error(errors)
            raise InputValidationException(AppErrorCodes.INVALID_INPUT, errors)

        return latitude, longitude, services

    def get_current_temperature(self, latitude: float, longitude: float,
                                      weather_services: list) -> tuple:
        """
        Gets weather from a given list of services and returns average of the temperature
        :param latitude:
        :param longitude:
        :param weather_services:
        :return: tuple (average_fahrenheit, average_celcius)
        """
        curr_temp_list = list()

        for service_name in weather_services:
            try:
                service = self.request.app['weather_services'][service_name]
                curr_temp_list.append(service.get_current_temperature(latitude, longitude))
            except WeatherServiceException as err:
                logging.exception(err)

        logging.info(curr_temp_list)
        curr_temp_list = [curr_temp for curr_temp in curr_temp_list if curr_temp]

        if not curr_temp_list:
            raise ServiceNotAvailable(AppErrorCodes.SERVICE_NOT_AVAILABLE,
                                      "No weather service available")

        average_fahrenheit = statistics.mean(curr_temp_list)
        average_celcius = round((average_fahrenheit - 32) * 5 / 9, 2)
        return average_fahrenheit, average_celcius

    async def get(self):
        """
        GET method handler for /current_weather
        :return:
        """
        query_params = dict(self.request.query)
        logging.info('Query params: %s', query_params)
        try:
            latitude, longitude, services = self.parse_request(query_params)
            fahrenheit, celcius = self.get_current_temperature(latitude, longitude, services)
            curr_dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            response = {
                'latitude': round(latitude, 2),
                'longitude': round(longitude, 2),
                'datetime': curr_dt,
                "services": services,
                'temperature': {
                    "fahrenheit": round(fahrenheit, 2),
                    "celsius": round(celcius, 2)
                }
            }
            logging.info(response)
            return web.json_response(response)

        except SureWeatherException as err:
            return web.Response(status=err.HTTP_CODE,
                                content_type="application/json",
                                text=json.dumps(err.to_dict()))


def add_routes(app: web.Application):
    """
    Add routes
    :param app:
    :return:
    """
    app.router.add_view("/current_weather", CurrentWeather)
