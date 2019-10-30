from abc import ABC
from abc import abstractmethod


class BaseWeatherService(ABC):
    """
    Base class for weather services
    """
    SERVICE_NAME = None
    BASE_URL_KEY = None

    @abstractmethod
    def get_current_temperature(self, latitude: float, longitude: float):
        pass
