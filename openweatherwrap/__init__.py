"""
OpenWeatherWrap
===========

A Python wrapper for the OpenWeatherMap API.
This library provides a simple interface to interact with the OpenWeatherMap API, allowing users to fetch weather data, forecasts, and other related information easily.

This module includes wrappers for most of the free OpenWeatherMap API endpoints, as well as synchronous and asynchronous implementations.
It is designed to be easy to use and integrate into Python applications.

Example usage:
```python
from openweatherwrap.api import OneCallAPI

API_KEY = "YOUR_API_KEY"
api = OneCallAPI(API_KEY, (37.7749, -122.4194), language="en", units="metric")
weather_data = api.get_current_weather()
# weather_data is an object containing functions to access the data provided by the API.
print(weather_data.get_current_temp())
```
"""

import requests # Using the checks from the library to check if it works

__version__ = "1.1.0"
__author__ = "lythox"
__license__ = "Attribution-ShareAlike 4.0 International"


__all__ = [
    "api",
    "asyncapi",
    "errors",
    "core"
]