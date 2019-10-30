from abc import ABC
from enum import unique, Enum
from http import HTTPStatus


@unique
class AppErrorCodes(Enum):
    '''
        Enum for HTTP Error Codes
        '''
    INVALID_INPUT = 3
    WEATHER_SERVICE_ERROR = 4
    GOOGLE_MAPS_ERROR = 5
    SERVICE_NOT_AVAILABLE = 6


class SureWeatherException(Exception, ABC):
    HTTP_CODE = HTTPStatus.INTERNAL_SERVER_ERROR.value

    def __init__(self, error_code: AppErrorCodes, message):
        self.error_code = error_code
        self.message = message
        super().__init__(message)

    def to_dict(self):
        return {
            "error_code": self.error_code.name,
            "error_message": self.message
        }


class InputValidationException(SureWeatherException):
    HTTP_CODE = HTTPStatus.BAD_REQUEST.value

    def __init__(self, error_code: AppErrorCodes, message: list):
        super().__init__(error_code, message)


class WeatherServiceException(SureWeatherException):
    HTTP_CODE = HTTPStatus.SERVICE_UNAVAILABLE.value

    def __init__(self, error_code: AppErrorCodes, message: str):
        super().__init__(error_code, message)


class ServiceNotAvailable(SureWeatherException):
    HTTP_CODE = HTTPStatus.SERVICE_UNAVAILABLE.value

    def __init__(self, error_code: AppErrorCodes, message: str):
        super().__init__(error_code, message)
