"""
Classes for handling OpenWeatherMap API requests.
These classes are designed to be used with the corresponding OpenWeatherMap API endpoints.

Example: If you want to use the One Call API, you can create an instance of the OneCallAPI class.
"""
import requests

from typing import Literal
from geopy.geocoders import Nominatim

from .core import AirPollutionResponse, CurrentWeatherResponse, GeocodingResponse, OneCallResponse, FiveDayForecastResponse, WeatherStation

from .errors import *

class OpenWeatherMapAPI:
    """
    Base class for OpenWeatherMap API wrappers.

    This class does not make any API calls itself, but provides common functionality for all OpenWeatherMap API wrappers.
    """
    def __init__(self, api_key: str, location: str | tuple, language: str='en', units: Literal['standard', 'metric', 'imperial'] = 'standard') -> None:
        """
        Base class for the OpenWeatherMap API wrapper.

        This class does not make any API calls itself, but provides common functionality for all OpenWeatherMap API wrappers.

        :param api_key: Your OpenWeatherMap API key.
        :param location: Location as a string (city name) or a tuple (latitude, longitude).
        :param language: Language for the API response (e.g., 'en', 'fr').
        :param units: Units for temperature ('standard', 'metric', 'imperial').

        :raises ValueError: If the location is not found when a string is provided.
        :raises ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
        :raises ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
        """
        self.api_key = api_key
        self.location = location
        self.language = language
        self.units = units

        if not isinstance(location, tuple):
            # Convert string location to tuple using geopy
            geolocator = Nominatim(user_agent="openweatherwrap")
            location_data = geolocator.geocode(location)
            if location_data:
                self.location = (location_data.latitude, location_data.longitude)
            else:
                raise ValueError("Location not found. Please provide a valid location.")
        else:
            if len(location) != 2 or not all(isinstance(coord, (int, float)) for coord in location):
                raise ValueError("Location must be a tuple of (latitude, longitude).")
            else:
                if not (-90 <= location[0] <= 90 and -180 <= location[1] <= 180):
                    raise ValueError("Latitude must be between -90 and 90, and longitude must be between -180 and 180.")

    def __str__(self) -> str:
        """
        Returns a string representation of the OneCallAPI instance.

        :return: String representation of the OneCallAPI instance.
        """
        return f"{self.__class__.__name__}(api_key={self.api_key}, location={self.location}, language={self.language}, units={self.units})"


class OneCallAPI(OpenWeatherMapAPI):
    """Wrapper for the One Call API from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard') -> None:
        """
        Initializes the OneCall API wrapper.

        This class provides access to the One Call API from OpenWeatherMap, which allows you to get current weather, minute-by-minute precipitation forecasts, hourly forecasts, daily forecasts, and weather alerts for a specific location.

        :param api_key: Your OpenWeatherMap API key.
        :param location: Location as a string (city name) or a tuple (latitude, longitude).
        :param language: Language for the API response (default is 'en').
        :param units: Units for temperature ('standard', 'metric', 'imperial').

        :raises ValueError: If the location is not found when a string is provided.
        :raises ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
        :raises ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
        """
        super().__init__(api_key, location, language, units)

        self.url = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={key}&lang={lang}&units={units}".format(
            lat=self.location[0],
            lon=self.location[1],
            key=self.api_key,
            lang=self.language,
            units=self.units
        )

    def get_weather(self, exclude: list[Literal['current', 'minutely', 'hourly', 'daily', 'alerts']] = []) -> OneCallResponse:
        """
        Fetches the weather data from the one call API and returns the response as a `OneCallResponse` object.
        The response includes all available weather data for the specified location.

        :param exclude: List of data types to exclude from the response. Options are 'current', 'minutely', 'hourly', 'daily', 'alerts'.

        :returns response: `OneCallResponse` object containing the weather data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        exclude_str = ','.join(exclude) if exclude else ''
        if exclude_str:
            url = self.url + f"&exclude={exclude_str}"
        else:
            url = self.url
        data = requests.get(url)
        if data.status_code == 200:
            return OneCallResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_timed_weather(self, timestamp: int) -> OneCallResponse:
        """
        Fetches the weather data for a specific timestamp from the one call API and returns the response as a `OneCallResponse` object.

        Data is available from January 1, 1979 up to 4 days ahead of the current date.

        :param timestamp: Unix timestamp for which to fetch the weather data.
        :returns response: `OneCallResponse` object containing the weather data for the specified timestamp.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        :raises ValueError: If the timestamp is before January 1, 1979.
        """
        if timestamp < 	283996800:  # January 1, 1979
            raise ValueError("Timestamp must be greater than or equal to January 1, 1979 (283996800).")
        url = f"{self.url.replace('onecall?', 'onecall/timemachine?')}&dt={timestamp}"
        data = requests.get(url)
        if data.status_code == 200:
            return OneCallResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_aggregation(self, date: str) -> OneCallResponse:
        """
        Fetches the weather data for a specific date from the one call API and returns the response as a `OneCallResponse` object.

        :param date: Date in the ISO 8601 format 'YYYY-MM-DD' for which to fetch the weather data.
        :returns response: `OneCallResponse` object containing the weather data for the specified date.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('onecall?', 'onecall/day_summary?')}&date={date}"
        data = requests.get(url)
        if data.status_code == 200:
            return OneCallResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_overview(self) -> str:
        """
        Fetches a brief, human-readable overview of the weather data for the specified location.

        :returns response: A string containing a brief overview of the weather data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('onecall?', 'onecall/overview?').replace(f'&lang={self.language}', '')}"
        data = requests.get(url)
        if data.status_code == 200:
            return data.json().get('weather_overview', 'No overview available.')
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

class CurrentWeatherAPI(OpenWeatherMapAPI):
    """Wrapper for the Current Weather Data API from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard', mode: Literal['xml', 'html', 'json']='json') -> None:
        """
        Initializes the CurrentWeatherData API wrapper.

        :param api_key: Your OpenWeatherMap API key.
        :param location: Location as a string (city name) or a tuple (latitude, longitude).
        :param language: Language for the API response (default is 'en').
        :param units: Units for temperature ('standard', 'metric', 'imperial').
        :param mode: Response format ('xml' or 'html'). If None, defaults to JSON.

        :raises ValueError: If the location is not found when a string is provided.
        :raises ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
        :raises ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
        :raises ValueError: If the mode is not 'xml' or 'html'.
        """
        super().__init__(api_key, location, language, units)
        self.mode = mode
        if self.mode not in ['xml', 'html', 'json']:
            raise ValueError("Mode must be either 'xml' or 'html' or 'json.")
        self.url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&lang={lang}&units={units}&mode={mode}".format(
            lat=self.location[0],
            lon=self.location[1],
            key=self.api_key,
            lang=self.language,
            units=self.units,
            mode=self.mode
        )

    def get_weather(self) -> str | CurrentWeatherResponse:
        """Fetches the current weather data from the OpenWeatherMap API and returns the response.

        Returns a string if the mode is 'html', otherwise returns a `CurrentWeatherResponse` object.

        :returns response: The response from the OpenWeatherMap API.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        data = requests.get(self.url)
        if data.status_code == 200:
            if self.mode == 'html':
                return data.text
            elif self.mode == 'xml':
                return CurrentWeatherResponse(data.content, self.mode)
            else:
                return CurrentWeatherResponse(data.json(), self.mode)
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

class FiveDayForecast(OpenWeatherMapAPI):
    """Fetches the 5-day / 3-hour weather forecast from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple, count: int = -1, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard', mode:Literal['json', 'xml']='json') -> None:
        """
        Initializes the FiveDayForecast API wrapper.

        :param api_key: Your OpenWeatherMap API key.
        :param location: Location as a string (city name) or a tuple (latitude, longitude).
        :param count: Number of forecast entries to return. If -1, returns all available entries.
        :param language: Language for the API response (default is 'en').
        :param units: Units for temperature ('standard', 'metric', 'imperial').
        :param mode: Response format ('xml'). If None, defaults to JSON.

        :raises ValueError: If the location is not found when a string is provided.
        :raises ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
        :raises ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
        :raises ValueError: If the mode is not 'xml'.
        """
        super().__init__(api_key, location, language, units)
        self.mode = mode
        self.count = count
        if self.mode not in ['xml', 'json']:
            raise ValueError("Mode must be either 'xml' or 'json'.")
        self.url = "https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}&lang={lang}&units={units}&mode={mode}".format(
            lat=self.location[0],
            lon=self.location[1],
            key=self.api_key,
            lang=self.language,
            units=self.units,
            mode=self.mode
        )
        if self.count > 0:
            self.url += f"&cnt={self.count}"

    def get_forecast(self) -> FiveDayForecastResponse:
        """
        Fetches the 5-day / 3-hour weather forecast from the OpenWeatherMap API and returns the response.

        :returns response: `FiveDayForecastResponse` object containing the forecast data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        data = requests.get(self.url)
        if data.status_code == 200:
            if self.mode == 'xml':
                return FiveDayForecastResponse(data.content, self.mode)
            else:
                return FiveDayForecastResponse(data.json(), self.mode)
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

class AirPollutionAPI(OpenWeatherMapAPI):
    """Wrapper for the Air Pollution API from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple) -> None:
        """
        Initializes the AirPollution API wrapper.

        :param api_key: Your OpenWeatherMap API key.
        :param location: Location as a string (city name) or a tuple (latitude, longitude).

        :raises ValueError: If the location is not found when a string is provided.
        :raises ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
        :raises ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
        """
        super().__init__(api_key, location)
        self.url = "https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}".format(
            lat=self.location[0],
            lon=self.location[1],
            key=self.api_key,
        )

    def get_current_air_pollution(self) -> AirPollutionResponse:
        """
        Fetches the current air pollution data from the OpenWeatherMap API and returns the response.

        :returns response: `AirPollutionResponse` object containing the air pollution data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        data = requests.get(self.url)
        if data.status_code == 200:
            return AirPollutionResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_air_pollution_forecast(self) -> AirPollutionResponse:
        """
        Fetches the air pollution forecast data from the OpenWeatherMap API and returns the response.

        :returns response: `AirPollutionResponse` object containing the air pollution forecast data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('air_pollution?', 'air_pollution/forecast?')}"
        data = requests.get(url)
        if data.status_code == 200:
            return AirPollutionResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_air_pollution_history(self, start: int, end: int) -> AirPollutionResponse:
        """
        Fetches the historical air pollution data from the OpenWeatherMap API for a specific time range and returns the response.

        :param start: Start timestamp (Unix time) for the historical data.
        :param end: End timestamp (Unix time) for the historical data.

        :returns response: `AirPollutionResponse` object containing the historical air pollution data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('air_pollution?', 'air_pollution/history?')}&start={start}&end={end}"
        data = requests.get(url)
        if data.status_code == 200:
            return AirPollutionResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

class GeocodingAPI(OpenWeatherMapAPI):
    """Wrapper for the Geocoding API from OpenWeatherMap."""
    def __init__(self, api_key: str) -> None:
        """
        Initializes the Geocoding API wrapper.

        :param api_key: Your OpenWeatherMap API key.
        :param location: Location as a string (city name) or a tuple (latitude, longitude).

        :raises ValueError: If the location is not found when a string is provided.
        :raises ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
        :raises ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
        """
        super().__init__(api_key, (0.0, 0.0))
        self.url = "https://api.openweathermap.org/geo/1.0/direct?&appid={key}".format(
            key=self.api_key
        )

    def get_by_city(self, city: str, country: str, state_code = None, limit=1) -> GeocodingResponse:
        """
        Fetches the geocoding data for a city and country from the OpenWeatherMap API and returns the response.

        State code applies only to the United States and is optional.

        :param city: City name.
        :param country: Country code (ISO 3166-1 alpha-2).
        :param state_code: Optional state code.

        :returns response: `GeocodingResponse` object containing the geocoding data.

        :raises ValueError: If limit > 5 or limit < 1.
        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        if limit > 5 or limit < 1:
            raise ValueError("Limit must be between 1 and 5.")
        url = f"{self.url}&q={city},{country}"
        if state_code:
            url += f",{state_code}"
        url += f"&limit={limit}"
        data = requests.get(url)
        if data.status_code == 200:
            return GeocodingResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_by_zip(self, zip_code: str, country: str) -> GeocodingResponse:
        """
        Fetches the geocoding data for a zip code and country from the OpenWeatherMap API and returns the response.

        :param zip_code: Zip code.
        :param country: Country code (ISO 3166-1 alpha-2).

        :returns response: `GeocodingResponse` object containing the geocoding data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace("direct?", "zip?")}&zip={zip_code},{country}"
        data = requests.get(url)
        if data.status_code == 200:
            return GeocodingResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

    def get_by_coordinates(self, latitude: float, longitude: float, limit=1) -> GeocodingResponse:
        """
        Fetches the geocoding data for a set of coordinates from the OpenWeatherMap API and returns the response.

        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :param limit: Number of results to return (default is 1, maximum is 5).

        :returns response: `GeocodingResponse` object containing the geocoding data.

        :raises ValueError: If limit > 5 or limit < 1.
        :raises ValueError: If latitude is not between -90 and 90, and longitude is not between -180 and 180.
        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        if limit > 5 or limit < 1:
            raise ValueError("Limit must be between 1 and 5.")
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Latitude must be between -90 and 90, and longitude must be between -180 and 180.")
        url = f"{self.url}&lat={latitude}&lon={longitude}&limit={limit}"
        url = url.replace('direct?', 'reverse?')
        data = requests.get(url)
        if data.status_code == 200:
            return GeocodingResponse(data.json())
        else:
            try:
                error_message = data.json().get('message', data.text)
            except Exception:
                error_message = data.text
            match data.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)

class WeatherStationAPI(OpenWeatherMapAPI):
    """Wrapper for the Weather Station API from OpenWeatherMap."""
    def __init__(self, api_key: str) -> None:
        """
        Initializes the Weather Station API wrapper.

        :param api_key: Your OpenWeatherMap API key.

        :raises ValueError: If the API key is not provided.
        """
        if not api_key:
            raise ValueError("API key must be provided.")
        super().__init__(api_key, (0.0, 0.0))
        self.url = "https://api.openweathermap.org/data/3.0/stations?appid={key}".format(
            key=self.api_key
        )
        self.headers = {
            'Content-Type': 'application/json'
        }

    def register_station(self, station_data: dict) -> WeatherStation:
        """
        Registers a new weather station with the OpenWeatherMap API.

        :param station_data: Dictionary containing the station data.

        :returns response: `WeatherStation` object containing the registered station data.

        :raises SubscriptionLevelError: If the API key does not have access to the requested data.
        :raises InvalidAPIKeyError: If the API key is invalid.
        :raises NotFoundError: If the location is not found.
        :raises TooManyRequestsError: If the API rate limit is exceeded.
        :raises OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = requests.post(self.url, json=station_data, headers=self.headers)
        if response.status_code == 201:
            return WeatherStation(response.json())
        else:
            try:
                error_message = response.json().get('message', response.text)
            except Exception:
                error_message = response.text
            match response.status_code:
                case 400000:
                    raise SubscriptionLevelError(error_message)
                case 401:
                    raise InvalidAPIKeyError(error_message)
                case 404:
                    raise NotFoundError(error_message)
                case 429:
                    raise TooManyRequestsError(error_message)
                case _:
                    raise OpenWeatherMapException(error_message)
