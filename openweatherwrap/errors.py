"""
A represantation for the different error codes provided by the API
"""

class OpenWeatherMapException:
    pass

class SubscriptionLevelError(OpenWeatherMapException):
    """Raised when requested data is not available under the current subscription plan (HTTP 400000)."""
    pass

class InvalidAPIKeyError(OpenWeatherMapException):
    """Raised when the API key provided is invalid (HTTP 401)"""
    pass

class NotFoundError(OpenWeatherMapException):
    """Raised when the location provided is invalid, or if the format of the request is wrong (HTTP 404)"""
    pass

class TooManyRequestsError(OpenWeatherMapException):
    """Raised when there are too many requests for the subscription (HTTP 429)"""
    pass
