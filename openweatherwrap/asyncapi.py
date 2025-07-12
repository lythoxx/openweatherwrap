"""
Classes for handling OpenWeatherMap API requests asnychronously.
These classes are designed to be used with the corresponding OpenWeatherMap API endpoints.

Example:
    If you want to use the One Call API, you can create an instance of the OneCallAPI class.
"""
from openweatherwrap._utils import _make_get_request_async
from .api import *

import aiohttp

from .core import OneCallAggregationResponse, OneCallResponse, OneCallTimestampedResponse, CurrentWeatherResponse, FiveDayForecastResponse, AirPollutionResponse, GeocodingResponse

class OneCallAPI(OpenWeatherMapAPI):
    """
    Asynchronous class for handling OpenWeatherMap One Call API requests.
    This class is designed to be used with the One Call API endpoint.
    """

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

    async def get_weather(self, exclude: list[Literal['current', 'minutely', 'hourly', 'daily', 'alerts']] = []) -> OneCallResponse:
        """
        Asynchronously fetches weather data from the One Call API.

        Args:
            exclude (list[Literal['current', 'minutely', 'hourly', 'daily', 'alerts']], optional): List of data types to exclude from the response.
                Defaults to an empty list, which means no data types are excluded.

        Returns:
            OneCallResponse: An instance of OneCallResponse containing the weather data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = f"{self.url}&exclude={','.join(exclude)}" if exclude else self.url
        response = await _make_get_request_async(url)
        return OneCallResponse(response)

    async def get_timed_weather(self, timestamp: int) -> OneCallTimestampedResponse:
        """
        Asynchronously fetches weather data for a specific timestamp from the One Call API.

        Args:
            timestamp (int): The Unix timestamp for which to fetch the weather data.

        Returns:
            OneCallResponse: An instance of OneCallResponse containing the weather data for the specified timestamp.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
            ValueError: If the timestamp is before January 1, 1979.
            ValueError: If the timestamp is not a valid UNIX timestamp.
        """
        if timestamp < 0:
            raise ValueError("Timestamp must be a positive integer representing seconds since January 1, 1970.")
        if timestamp < 283996800:  # January 1, 1979
            raise ValueError("Timestamp must be greater than or equal to January 1, 1979 (283996800).")
        url = self.url.replace('onecall?', 'onecall/timemachine?')
        url += f"&dt={timestamp}"
        response = await _make_get_request_async(url)
        return OneCallTimestampedResponse(response)

    async def get_aggregation(self, date: str) -> OneCallAggregationResponse:
        """
        Asynchronously fetches the weather data for a specific date from the one call API and returns the response as a `OneCallResponse` object`.

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
        url = self.url.replace('onecall?', 'onecall/day_summary?')
        url += f"&date={date}"
        response = await _make_get_request_async(url)
        return OneCallAggregationResponse(response)

    async def get_overview(self) -> str:
        """
        Asynchronously fetches a brief, human-readable overview of the weather data for the specified location.

        Returns:
            str: A brief overview of the weather data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = self.url.replace('onecall?', 'onecall/overview?')
        response = await _make_get_request_async(url, json=True)
        return response.get("weather_overview", "No overview available.")

class CurrentWeatherAPI(OpenWeatherMapAPI):
    """
    Asynchronous class for handling OpenWeatherMap Current Weather API requests.
    This class is designed to be used with the Current Weather API endpoint.
    """
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

        if mode not in ['xml', 'html', 'json']:
            raise ValueError("Mode must be one of 'xml', 'html', or 'json'.")

        self.mode = mode
        self.url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&lang={lang}&units={units}&mode={mode}".format(
            lat=self.location[0],
            lon=self.location[1],
            key=self.api_key,
            lang=self.language,
            units=self.units,
            mode=self.mode
        )

    async def get_weather(self) -> str | CurrentWeatherResponse:
        """
        Asynchronously fetches current weather data from the Current Weather API.

        Returns:
            str | CurrentWeatherResponse: An instance of CurrentWeatherResponse containing the current weather data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = await _make_get_request_async(self.url, json=(self.mode == 'json'))
        if self.mode != 'html':
            return CurrentWeatherResponse(response, mode=self.mode)
        else:
            return response

class FiveDayForecast(OpenWeatherMapAPI):
    """
    Asynchronous class for handling OpenWeatherMap 5-Day Forecast API requests.
    This class is designed to be used with the 5-Day Forecast API endpoint.
    """

    def __init__(self, api_key: str, location: str | tuple, count: int = -1, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard', mode:Literal['json', 'xml']='json') -> None:
        """
        Initializes the FiveDayForecast API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
            location (str | tuple): Location as a string (city name) or a tuple (latitude, longitude).
            count (int, optional): Number of forecast entries to return. Defaults to -1, which returns all available entries.
            language (str, optional): Language for the API response (default is 'en').
            units (Literal['standard', 'metric', 'imperial'], optional): Units for temperature ('standard', 'metric', 'imperial').
            mode (Literal['json', 'xml'], optional): Response format ('json' or 'xml'). Defaults to 'json'.

        Raises:
            ValueError: If the location is not found when a string is provided.
            ValueError: If the location tuple is not valid (not a tuple of two floats or ints).
            ValueError: If the latitude is not between -90 and 90, and longitude is not between -180 and 180.
            ValueError: If the mode is not 'json' or 'xml'.
        """
        super().__init__(api_key, location, language, units)

        if mode not in ['json', 'xml']:
            raise ValueError("Mode must be one of 'json' or 'xml'.")

        self.mode = mode
        self.count = count
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

    async def get_forecast(self) -> FiveDayForecastResponse:
        """
        Asynchronously fetches the 5-day weather forecast data from the 5-Day Forecast API.

        Returns:
            FiveDayForecastResponse: An instance of FiveDayForecastResponse containing the forecast data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = await _make_get_request_async(self.url, json=(self.mode == 'json'))
        return FiveDayForecastResponse(response, mode=self.mode)

class AirPollutionAPI(OpenWeatherMapAPI):
    """
    Asynchronous class for handling OpenWeatherMap Air Pollution API requests.
    This class is designed to be used with the Air Pollution API endpoint.
    """

    def __init__(self, api_key: str, location: str | tuple, language: str = 'en', units: Literal['standard', 'metric', 'imperial'] = 'standard') -> None:
        """
        Initializes the AirPollution API wrapper.

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
        super().__init__(api_key, location)

        self.url = "https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}".format(
            lat=self.location[0],
            lon=self.location[1],
            key=self.api_key
        )

    async def get_air_pollution(self) -> AirPollutionResponse:
        """
        Asynchronously fetches air pollution data from the Air Pollution API.

        Returns:
            AirPollutionResponse: An instance of AirPollutionResponse containing the air pollution data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        response = await _make_get_request_async(self.url)
        return AirPollutionResponse(response)

    async def get_air_pollution_forecast(self) -> AirPollutionResponse:
        """
        Asynchronously fetches air pollution forecast data from the Air Pollution API.

        Returns:
            AirPollutionResponse: An instance of AirPollutionResponse containing the air pollution forecast data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = self.url.replace('air_pollution?', 'air_pollution/forecast?')
        response = await _make_get_request_async(url)
        return AirPollutionResponse(response)

    async def get_air_pollution_history(self, start: int, end: int) -> AirPollutionResponse:
        """
        Asynchronously fetches historical air pollution data from the Air Pollution API.

        Args:
            start (int): Start time in UNIX timestamp format.
            end (int): End time in UNIX timestamp format.

        Returns:
            AirPollutionResponse: An instance of AirPollutionResponse containing the historical air pollution data.

        Raises:
            SubscriptionLevelError: If the API key does not have access to the requested data.
            InvalidAPIKeyError: If the API key is invalid.
            NotFoundError: If the location is not found.
            TooManyRequestsError: If the API rate limit is exceeded.
            OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
        """
        url = self.url.replace('air_pollution?', 'air_pollution/history?')
        url += f"&start={start}&end={end}"
        response = await _make_get_request_async(url)
        return AirPollutionResponse(response)

class GeocodingAPI(OpenWeatherMapAPI):
    """
    Asynchronous class for handling OpenWeatherMap Geocoding API requests.
    This class is designed to be used with the Geocoding API endpoint.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the Geocoding API wrapper.

        Args:
            api_key (str): Your OpenWeatherMap API key.
        """
        super().__init__(api_key, (0.0, 0.0))

        self.url = "https://api.openweathermap.org/geo/1.0/direct?appid={key}&q=".format(
            key=self.api_key
        )

    async def get_by_city(self, city: str, country: str, state_code = None, limit=1) -> GeocodingResponse:
        """
        Fetches geocoding data for a city and country.

        Args:
            city (str): The name of the city.
            country (str): The country code (ISO 3166-1 alpha-2).
            state_code (str, optional): The state code, only for US states.
            limit (int, optional): Maximum number of results to return. Defaults to 1.

        Returns:
            GeocodingResponse: An instance of GeocodingResponse containing the geocoding data.
        """
        url = self.url + f"{city},{state_code},{country}" if state_code else self.url + f"{city},{country}"
        url += f"&limit={limit}"
        response = await _make_get_request_async(url)
        return GeocodingResponse(response)

    async def get_by_zip(self, zip_code: str, country: str) -> GeocodingResponse:
        """
        Fetches geocoding data for a zip code and country.

        Args:
            zip_code (str): The zip code.
            country (str): The country code (ISO 3166-1 alpha-2).

        Returns:
            GeocodingResponse: An instance of GeocodingResponse containing the geocoding data.
        """
        url = f"{self.url}{zip_code},{country}"
        response = await _make_get_request_async(url)
        return GeocodingResponse(response)

    async def get_by_coordinates(self, latitude: float, longitude: float, limit: int = 1) -> GeocodingResponse:
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
        url = f"{self.url.replace("&q=", "")}&lat={latitude}&lon={longitude}&limit={limit}"
        url = url.replace('direct?', 'reverse?')
        response = await _make_get_request_async(url)
        return GeocodingResponse(response)

class WeatherMapsAPI(OpenWeatherMapAPI):
    """
    Asynchronous class for handling OpenWeatherMap Weather Map API requests.
    This class is designed to be used with the Weather Map API endpoint.
    """
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

    async def get_weathermap(self, layer: Literal["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "wind_new"], x: int, y: int, zoom: int) -> bytes:
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
        response = await _make_get_request_async(url, json=False)
        return response

    async def download_weathermap(self, layer: Literal["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new", "snow_new", "rain_new"], x: int, y: int, zoom: int, filename: str) -> None:
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
        image_data = await self.get_weathermap(layer, x, y, zoom)
        with open(filename, 'wb') as file:
            file.write(image_data)