"""
A representation for the different error codes provided by the API
"""

class OpenWeatherMapException(Exception):
    """Base class for all OpenWeatherMap exceptions."""
    def __init__(self, message: str = "An error occurred with the OpenWeatherMap API."):
        super().__init__(message)

class SubscriptionLevelError(OpenWeatherMapException):
    """Raised when requested data is not available under the current subscription plan (HTTP 400000)."""
    def __init__(self, message: str = "Requested data is not available under the current subscription plan (HTTP 400000)."):
        super().__init__(message)

class InvalidAPIKeyError(OpenWeatherMapException):
    """Raised when the API key provided is invalid (HTTP 401)"""
    def __init__(self, message: str = "The API key provided is invalid (HTTP 401)."):
        super().__init__(message)

class NotFoundError(OpenWeatherMapException):
    """Raised when the location provided is invalid, or if the format of the request is wrong (HTTP 404)"""
    def __init__(self, message: str = "The location provided is invalid, or the request format is wrong (HTTP 404)."):
        super().__init__(message)

class TooManyRequestsError(OpenWeatherMapException):
    """Raised when there are too many requests for the subscription (HTTP 429)"""
    def __init__(self, message: str = "Too many requests for the subscription (HTTP 429)."):
        super().__init__(message)
