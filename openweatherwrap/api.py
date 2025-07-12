"""
Classes for handling OpenWeatherMap API requests.
These classes are designed to be used with the corresponding OpenWeatherMap API endpoints.

Example:
    If you want to use the One Call API, you can create an instance of the OneCallAPI class.
"""
import requests

from typing import Literal
from geopy.geocoders import Nominatim

from openweatherwrap._utils import _make_get_request

from .core import AirPollutionResponse, CurrentWeatherResponse, GeocodingResponse, OneCallResponse, FiveDayForecastResponse, OneCallTimestampedResponse, OneCallAggregationResponse

from .errors import *

class OpenWeatherMapAPI:
    """
    Base class for OpenWeatherMap API wrappers.

    This class does not make any API calls itself, but provides common functionality for all OpenWeatherMap API wrappers.
    """
    def __init__(self, api_key: str, location: str | tuple, language: str='en', units: Literal['standard', 'metric', 'imperial'] = 'standard') -> None:
        """
        Base class for the OpenWeatherMap API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
            location (str | tuple): Location as a string (city name) or a tuple (latitude, longitude).
            language (str, optional): Language for the API response (e.g., 'en', 'fr'). Defaults to 'en'.
            units (Literal['standard', 'metric', 'imperial'], optional): Units for temperature ('standard', 'metric', 'imperial'). Defaults to 'standard'.

        Raises:
            ValueError: If the location is not found when a string is provided.
            ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
            ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
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
        Returns a string representation of the API instance.

        Returns:
            str: String representation of the API instance.
        """
        return f"{self.__class__.__name__}(api_key={self.api_key}, location={self.location}, language={self.language}, units={self.units})"


class OneCallAPI(OpenWeatherMapAPI):
    """Wrapper for the One Call API from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard') -> None:
        """
        Initializes the OneCall API wrapper.

        This class provides access to the One Call API from OpenWeatherMap, which allows you to get current weather, minute-by-minute precipitation forecasts, hourly forecasts, daily forecasts, and weather alerts for a specific location.

        Args:
            api_key (str): Your OpenWeatherMap API key.
            location (str | tuple): Location as a string (city name) or a tuple (latitude, longitude).
            language (str, optional): Language for the API response (default is 'en').
            units (Literal['standard', 'metric', 'imperial'], optional): Units for temperature ('standard', 'metric', 'imperial').

        Raises:
            ValueError: If the location is not found when a string is provided.
            ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
            ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
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
        Fetches the weather data from the one call API and returns the response as a `OneCallResponse` object`.
        The response includes all available weather data for the specified location.

        Args:
            exclude (list[Literal['current', 'minutely', 'hourly', 'daily', 'alerts']], optional): List of data types to exclude from the response. Options are 'current', 'minutely', 'hourly', 'daily', 'alerts'.

        Returns:
            OneCallResponse: Object containing the weather data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        exclude_str = ','.join(exclude) if exclude else ''
        if exclude_str:
            url = self.url + f"&exclude={exclude_str}"
        else:
            url = self.url
        response = _make_get_request(url)
        return OneCallResponse(response.json())

    def get_timed_weather(self, timestamp: int) -> OneCallTimestampedResponse:
        """
        Fetches the weather data for a specific timestamp from the one call API and returns the response as a `OneCallResponse` object`.

        Data is available from January 1, 1979 up to 4 days ahead of the current date.

        Args:
            timestamp (int): Unix timestamp for which to fetch the weather data.

        Returns:
            OneCallResponse: Object containing the weather data for the specified timestamp.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
            ValueError: If the timestamp is before January 1, 1979.
        """
        if timestamp < 283996800:  # January 1, 1979
            raise ValueError("Timestamp must be greater than or equal to January 1, 1979 (283996800).")
        url = f"{self.url.replace('onecall?', 'onecall/timemachine?')}&dt={timestamp}"
        response = _make_get_request(url)
        return OneCallTimestampedResponse(response.json())

    def get_aggregation(self, date: str) -> OneCallAggregationResponse:
        """
        Fetches the weather data for a specific date from the one call API and returns the response as a `OneCallResponse` object`.

        Args:
            date (str): Date in the `ISO 8601`_ format 'YYYY-MM-DD' for which to fetch the weather data.

        Returns:
            OneCallResponse: Object containing the weather data for the specified date.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).

        .. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
        """
        url = f"{self.url.replace('onecall?', 'onecall/day_summary?')}&date={date}"
        response = _make_get_request(url)
        return OneCallAggregationResponse(response.json())

    def get_overview(self) -> str:
        """
        Fetches a brief, human-readable overview of the weather data for the specified location.

        Returns:
            str: A string containing a brief overview of the weather data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('onecall?', 'onecall/overview?').replace(f'&lang={self.language}', '')}"
        response = _make_get_request(url)
        return response.json().get('weather_overview', 'No overview available.')

class CurrentWeatherAPI(OpenWeatherMapAPI):
    """Wrapper for the Current Weather Data API from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard', mode: Literal['xml', 'html', 'json']='json') -> None:
        """
        Initializes the CurrentWeatherData API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
            location (str | tuple): Location as a string (city name) or a tuple (latitude, longitude).
            language (str, optional): Language for the API response (default is 'en').
            units (Literal['standard', 'metric', 'imperial'], optional): Units for temperature ('standard', 'metric', 'imperial').
            mode (Literal['xml', 'html', 'json'], optional): Response format ('xml', 'html', or 'json'). Defaults to 'json'.

        Raises:
            ValueError: If the location is not found when a string is provided.
            ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
            ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
            ValueError: If the mode is not 'xml', 'html', or 'json'.
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
        """
        Fetches the current weather data from the OpenWeatherMap API and returns the response.

        Returns:
            str | CurrentWeatherResponse: Returns a string if the mode is 'html', otherwise returns a `CurrentWeatherResponse` object.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = _make_get_request(self.url)
        if self.mode == 'html':
            return response.text
        elif self.mode == 'xml':
            return CurrentWeatherResponse(response.content, self.mode)
        else:
            return CurrentWeatherResponse(response.json(), self.mode)

class FiveDayForecast(OpenWeatherMapAPI):
    """Fetches the 5-day / 3-hour weather forecast from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple, count: int = -1, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard', mode:Literal['json', 'xml']='json') -> None:
        """
        Initializes the FiveDayForecast API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
            location (str | tuple): Location as a string (city name) or a tuple (latitude, longitude).
            count (int, optional): Number of forecast entries to return. If -1, returns all available entries.
            language (str, optional): Language for the API response (default is 'en').
            units (Literal['standard', 'metric', 'imperial'], optional): Units for temperature ('standard', 'metric', 'imperial').
            mode (Literal['json', 'xml'], optional): Response format ('xml' or 'json'). Defaults to 'json'.

        Raises:
            ValueError: If the location is not found when a string is provided.
            ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
            ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
            ValueError: If the mode is not 'xml' or 'json'.
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

        Returns:
            FiveDayForecastResponse: Object containing the forecast data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = _make_get_request(self.url)
        if self.mode == 'xml':
            return FiveDayForecastResponse(response.content, self.mode)
        else:
            return FiveDayForecastResponse(response.json(), self.mode)

class AirPollutionAPI(OpenWeatherMapAPI):
    """Wrapper for the Air Pollution API from OpenWeatherMap."""
    def __init__(self, api_key: str, location: str | tuple) -> None:
        """
        Initializes the AirPollution API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
            location (str | tuple): Location as a string (city name) or a tuple (latitude, longitude).

        Raises:
            ValueError: If the location is not found when a string is provided.
            ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
            ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
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

        Returns:
            AirPollutionResponse: Object containing the air pollution data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = _make_get_request(self.url)
        return AirPollutionResponse(response.json())

    def get_air_pollution_forecast(self) -> AirPollutionResponse:
        """
        Fetches the air pollution forecast data from the OpenWeatherMap API and returns the response.

        Returns:
            AirPollutionResponse: Object containing the air pollution forecast data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('air_pollution?', 'air_pollution/forecast?')}"
        response = _make_get_request(url)
        return AirPollutionResponse(response.json())

    def get_air_pollution_history(self, start: int, end: int) -> AirPollutionResponse:
        """
        Fetches the historical air pollution data from the OpenWeatherMap API for a specific time range and returns the response.

        Args:
            start (int): Start timestamp (Unix time) for the historical data.
            end (int): End timestamp (Unix time) for the historical data.

        Returns:
            AirPollutionResponse: Object containing the historical air pollution data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url.replace('air_pollution?', 'air_pollution/history?')}&start={start}&end={end}"
        response = _make_get_request(url)
        return GeocodingResponse(response.json())

class GeocodingAPI(OpenWeatherMapAPI):
    """Wrapper for the Geocoding API from OpenWeatherMap."""
    def __init__(self, api_key: str) -> None:
        """
        Initializes the Geocoding API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
        """
        super().__init__(api_key, (0.0, 0.0))
        self.url = "https://api.openweathermap.org/geo/1.0/direct?&appid={key}".format(
            key=self.api_key
        )

    def get_by_city(self, city: str, country: str, state_code = None, limit=1) -> GeocodingResponse:
        """
        Fetches the geocoding data for a city and country from the OpenWeatherMap API and returns the response.

        State code applies only to the United States and is optional.

        Args:
            city (str): City name.
            country (str): Country code (`ISO 3166-1 alpha-2`).
            state_code (str, optional): Optional state code.
            limit (int, optional): Number of results to return. Defaults to 1.

        Returns:
            GeocodingResponse: Object containing the geocoding data.

        Raises:
            ValueError: If limit > 5 or limit < 1.
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).

        .. _ISO 3166-1 alpha-2: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        """
        if limit > 5 or limit < 1:
            raise ValueError("Limit must be between 1 and 5.")
        url = f"{self.url}&q={city},{country}"
        if state_code:
            url += f",{state_code}"
        url += f"&limit={limit}"
        response = _make_get_request(url)
        return GeocodingResponse(response.json())

    def get_by_zip(self, zip_code: str, country: str) -> GeocodingResponse:
        """
        Fetches the geocoding data for a zip code and country from the OpenWeatherMap API and returns the response.

        Args:
            zip_code (str): Zip code.
            country (str): Country code (`ISO 3166-1 alpha-2`_).

        Returns:
            GeocodingResponse: Object containing the geocoding data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).

        .. _ISO 3166-1 alpha-2: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        """
        url = f"{self.url.replace("direct?", "zip?")}&zip={zip_code},{country}"
        response = _make_get_request(url)
        return GeocodingResponse(response.json())

    def get_by_coordinates(self, latitude: float, longitude: float, limit: int = 1) -> GeocodingResponse:
        """
        Fetches the geocoding data for a set of coordinates from the OpenWeatherMap API and returns the response.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.
            limit (int, optional): Number of results to return (default is 1, maximum is 5).

        Returns:
            GeocodingResponse: Object containing the geocoding data.

        Raises:
            ValueError: If limit > 5 or limit < 1.
            ValueError: If latitude is not between -90 and 90, and longitude is not between -180 and 180.
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        if limit > 5 or limit < 1:
            raise ValueError("Limit must be between 1 and 5.")
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Latitude must be between -90 and 90, and longitude must be between -180 and 180.")
        url = f"{self.url}&lat={latitude}&lon={longitude}&limit={limit}"
        url = url.replace('direct?', 'reverse?')
        response = _make_get_request(url)
        return GeocodingResponse(response.json())

class WeatherMapsAPI(OpenWeatherMapAPI):
    """Wrapper for the Weather Map API from OpenWeatherMap."""
    def __init__(self, api_key: str) -> None:
        """
        Initializes the Weather Map API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.

        """
        super().__init__(api_key, (0.0, 0.0))
        self.url = "https://tile.openweathermap.org/map/LAYER/Z/X/Y.png?appid={key}".format(
            key=self.api_key,
        )

    def get_weathermap(self, layer: Literal["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "wind_new"], x: int, y: int, zoom: int) -> bytes:
        """
        Fetches the weather map image for a specific layer and coordinates.

        The pixel coordinate can be calculated using the following formula:

        .. math::
            pixel = world\_coordinate * 2^{zoom}

        You can read more `here`_.

        Args:
            layer (Literal["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "snow_new", "rain_new"]): The layer to fetch.
            x (int): X coordinate of the tile.
            y (int): Y coordinate of the tile.
            zoom (int): Zoom level.

        Returns:
            bytes: The weather map image data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
            ValueError: If the layer is not one of the supported layers.
            ValueError: if zoom is not between 0 and 9 (inclusive).
            ValueError: if the x and y coordinates are not valid.

        .. _here: https://developers.google.com/maps/documentation/javascript/coordinates?hl=en#pixel-coordinates
        """
        if not (0 <= zoom <= 9):
            raise ValueError("Zoom must be between 0 and 9 (inclusive).")
        if not (isinstance(x, int) and isinstance(y, int)):
            raise ValueError("X and Y coordinates must be integers.")
        if zoom == 0 and (x != 1 or y != 1):
            raise ValueError("For zoom level 0, x and y must be 1.")
        if x > 2**zoom - 1 or y > 2**zoom - 1:
            raise ValueError("X and Y coordinates must be within the valid range for the specified zoom level.")
        if x < 0 or y < 0:
            raise ValueError("X and Y coordinates must be non-negative integers.")
        if layer not in ["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "wind_new"]:
            raise ValueError("Layer must be one of: 'clouds_new', 'precipitation_new', 'pressure_new', 'wind_new', 'temp_new', 'snow_new', 'rain_new'.")
        url = self.url.replace("LAYER", layer).replace("X", str(x)).replace("Y", str(y)).replace("Z", str(zoom))
        response = _make_get_request(url)
        return response.content

    def download_weathermap(self, layer: Literal["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "snow_new", "rain_new"], x: int, y: int, zoom: int, filename: str) -> None:
        """
        Downloads the weather map image for a specific layer and coordinates to a file.

        The pixel coordinate can be calculated using the following formula:

        .. math::
            pixel\_coordinate = world\_coordinate * 2^{zoom}

        You can read more `here`_.

        Args:
            layer (Literal["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "snow_new", "rain_new"]): The layer to fetch.
            x (int): X coordinate of the tile.
            y (int): Y coordinate of the tile.
            zoom (int): Zoom level.
            filename (str): The name of the file to save the image to.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
            ValueError: If the layer is not one of the supported layers.
            ValueError: if zoom is not between 0 and 9 (inclusive).
            ValueError: if the x and y coordinates are not valid.
            OSError: If there is an error writing to the file.

        .. _here: https://developers.google.com/maps/documentation/javascript/coordinates?hl=en#pixel-coordinates
        """
        image_data = self.get_weathermap(layer, x, y, zoom)
        with open(filename, 'wb') as file:
            file.write(image_data)