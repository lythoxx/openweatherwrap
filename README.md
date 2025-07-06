# OpenWeatherWrap

OpenWeatherWrap is an unofficial wrapper for the OpenWeatherMap API.

## Endpoints included in the wrapper

- One Call API 3.0
- Current Weather API
- 3-hour Forecast 5 days
- Air Pollution API
- Geocoding API
- Weather Maps 1.0

## Getting Started

To install this package run

```shell
pip install openweatherwrap
```

To start fetching weather data, make sure you have an API-key from [OpenWeatherMap](https://openweathermap.org/).

## Examples

### One Call API

```python
from openweatherwrap.api import OneCallAPI

# Create an instance of the API
api = OneCallAPI(API_KEY, "London, England", units="metric")
# Get only the current weather
response = api.get_weather(exclude=["minutely", "hourly", "daily", "alerts"])
#Access the data
print(f"The current temperature in London is {response.get_current_temp()}°C.")
print(f"The temperature feels like {response.get_current_feels_like()}°C")
```

### Current Weather API

```python
from openweatherwrap.api import CurrentWeatherAPI

# Create an instance of the API
api = CurrentWeatherAPI(API_KEY, "London, England", units='imperial')
# Getting the data
response = api.get_weather()
print(f"The current wind speed in London is {response.get_wind_speed()} miles per hour.")
```

### 5-Day/3-Hour Forecast

```python
from openweatherwrap.api import FiveDayForecast

# Create an instance of the API
api = FiveDayForecast(API_KEY, "London, England", mode='xml')
# Getting the forecast
response = api.get_forecast()
temperature_sorted = sorted(response.get_temperature())
print(f"During the following five days, London will experience temperatures from {temperature_sorted[0]} Kelvin to {temperature_sorted[-1]} Kelvin")
```

### Air Pollution API

```python
from openweatherwrap.api import AirPollutionAPI

# Create an instance of the API
api = AirPollutionAPI(API_KEY, "London, England")
# Getting the current air pollution
response = api.get_current_air_pollution()
print(f"London currently has an AQI of {response.get_aqi()} and has {response.get_nitrogen_dioxide()}µg/m³ of NO₂.")
```

### Geocoding API

```python
from openweatherwrap.api import GeocodingAPI

# Create an instance of the API
api = GeocodingAPI(API_KEY)
# Getting the data
response = api.get_by_city("London", "England")
print(f"London has a latitude of {response.get_latitude()}° and a longitude of {response.get_longitude()}°")
```

### Async

OpenWeatherWrap also includes asynchronous handling of the OpenWeatherMap API.

The usage is almost the same as the synchronous handler.

```python
from openweatherwrap.asyncapi import OneCallAPI
import asyncio

async def onecall_example():
    # Create an instance of the API
    api = OneCallAPI(API_KEY, "London, England", units="metric")
    # Get only the current weather
    response = await api.get_weather(exclude=["minutely", "hourly", "daily", "alerts"])
    #Access the data
    print(f"The current temperature in London is {response.get_current_temp()}°C.")
    print(f"The temperature feels like {response.get_current_feels_like()}°C")

if __name__ == "__main__":
    asyncio.run(onecall_example())
```

## Attribution

Weather data provided by [OpenWeather](https://openweathermap.org/)
