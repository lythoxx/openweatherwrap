"""
Utility functions for OpenWeatherWrap.

This module provides helper functions to assist with the OpenWeatherWrap library, and is not intended for direct use by end users.
"""
import requests
import aiohttp

from openweatherwrap.errors import InvalidAPIKeyError, NotFoundError, OpenWeatherMapException, SubscriptionLevelError, TooManyRequestsError

def _make_get_request(url) -> requests.Response:
    """
    Make a synchronous GET request to the specified URL with the given parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (dict): The parameters to include in the GET request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        SubscriptionLevelError: If the API key does not have access to the requested data.
        InvalidAPIKeyError: If the API key is invalid.
        NotFoundError: If the location is not found.
        TooManyRequestsError: If the API rate limit is exceeded.
        OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
    """
    data = requests.get(url)
    if data.status_code == 200:
        return data
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


async def _make_get_request_async(url, json: bool = True) -> dict | str | bytes:
    """
    Make an asynchronous GET request to the specified URL.

    Args:
        url (str): The URL to send the GET request to.
        json (bool): If True, the response will be parsed as JSON. If False, the raw response text or bytes will be returned.

    Returns:
        dict: The JSON-decoded response data.

    Raises:
        SubscriptionLevelError: If the API key does not have access to the requested data.
        InvalidAPIKeyError: If the API key is invalid.
        NotFoundError: If the location is not found.
        TooManyRequestsError: If the API rate limit is exceeded.
        OpenWeatherMapException: For internal server errors (500, 502, 503, 504).
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                if json:
                    return await response.json()
                else:
                    try:
                        return await response.text()
                    except UnicodeDecodeError: # Return raw bytes if text decoding fails
                        return await response.read()
            else:
                try:
                    error_message = await response.json()
                except Exception:
                    error_message = await response.text()
                match response.status:
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