import logging

from .weatherdotcom import WeatherDotCom
from .accuweather import AccuWeather
from .noaa import NoaaWeather


def get_available_weather_services():

    def _add_service(service_class, name: str):
        try:
            logging.info("Adding Weather service: %s", name)
            service_obj = service_class()
            if service_obj:
                logging.info("%s added", name)
                return service_obj

            logging.info("%s not available", name)
        except KeyError as err:
            logging.info("%s not available", name)
            logging.exception(err)

        return None

    weather_services = dict()

    weather_services[WeatherDotCom.SERVICE_NAME] = _add_service(WeatherDotCom,
                                                                WeatherDotCom.SERVICE_NAME)
    weather_services[AccuWeather.SERVICE_NAME] = _add_service(AccuWeather,
                                                              AccuWeather.SERVICE_NAME)
    weather_services[NoaaWeather.SERVICE_NAME] = _add_service(NoaaWeather,
                                                              NoaaWeather.SERVICE_NAME)

    return {key: val for key, val in weather_services.items() if val}
