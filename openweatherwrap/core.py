from typing import Literal
import xml.etree.ElementTree as ET

class OpenWeatherAlert:
    """A class to represent an alert from the OpenWeather API."""
    def __init__(self, data: dict):
        """
        Initializes the OpenWeatherAlert with the provided data.

        :param data: A dictionary containing the alert data.
        """
        self.sender_name = data.get('sender_name', None)
        self.event = data.get('event', None)
        self.start = data.get('start', None)
        self.end = data.get('end', None)
        self.description = data.get('description', None)
        self.tags = data.get('tags', [])

    def get_sender_name(self) -> str | None:
        """Returns the name of the sender of the alert.

        :return sender_name: Sender name as a string or None if not available.
        """
        return self.sender_name

    def get_event(self) -> str | None:
        """Returns the event type of the alert.

        :return event: Event type as a string or None if not available.
        """
        return self.event

    def get_start(self) -> int | None:
        """Returns the start time of the alert in Unix timestamp format.

        :return start: Start time as an integer (timestamp) or None if not available.
        """
        return self.start

    def get_end(self) -> int | None:
        """Returns the end time of the alert in Unix timestamp format.

        :return end: End time as an integer (timestamp) or None if not available.
        """
        return self.end

    def get_description(self) -> str | None:
        """Returns a description of the alert.

        :return description: Description of the alert as a string or None if not available.
        """
        return self.description

    def get_tags(self) -> list[str]:
        """Returns a list of tags associated with the alert.

        :return tags: List of tags as strings. If no tags are available, returns an empty list.
        """
        return self.tags

class OneCallResponse:
    """A class to handle the response from the OpenWeather One Call API."""
    def __init__(self, data):
        """
        Initializes the OneCallResponse with the provided data.

        :param data: A dictionary containing the response data from the One Call API.
        """
        self.data = data

    def get_latitude(self) -> float:
        """
        Returns the latitude from the response data.
        Latitude will be a value between -90 and 90.

        :return latitude: Latitude as a float.
        """
        return self.data.get('lat', 0.0)

    def get_longitude(self) -> float:
        """
        Returns the longitude from the response data.
        Longitude will be a value between -180 and 180.

        :return longitude: Longitude as a float.
        """
        return self.data.get('lon', 0.0)

    def get_timezone(self) -> str:
        """
        Returns the timezone from the response data.
        Timezone is a string representing the timezone of the location.
        Example: 'America/New_York'

        :return timezone: Timezone as a string.
        """
        return self.data.get('timezone', 'UTC')

    def get_timezone_offset(self) -> int:
        """
        Returns the timezone offset from the response data.
        Timezone offset is the difference in seconds from UTC.
        Example: -14400 for UTC-4 (Eastern Daylight Time).

        :return timezone_offset: Timezone offset as an integer.
        """
        return self.data.get('timezone_offset', 0)

    def get_current_time(self) -> int | None:
        """
        Returns the current time in seconds since the epoch from the response data.
        This is the time of the current weather data.

        :return current_time: Current time as an integer (timestamp).
        """
        return self.data.get('current', {}).get('dt', None)

    def get_current_sunrise(self) -> int | None:
        """
        Returns the sunrise time in seconds since the epoch from the response data.
        This is the time of sunrise for the current day.

        :return sunrise: Sunrise time as an integer (timestamp).
        """
        return self.data.get('current', {}).get('sunrise', None)

    def get_current_sunset(self) -> int | None:
        """
        Returns the sunset time in seconds since the epoch from the response data.
        This is the time of sunset for the current day.

        :return sunset: Sunset time as an integer (timestamp).
        """
        return self.data.get('current', {}).get('sunset', None)

    def get_current_temp(self) -> float | None:
        """
        Returns the current temperature from the response data.
        Temperature is in Kelvin by default, but can be converted to Celsius or Fahrenheit as needed.

        :return temp: Current temperature as a float.
        """
        return self.data.get('current', {}).get('temp', None)

    def get_current_feels_like(self) -> float | None:
        """
        Returns the current feels-like temperature from the response data.
        Feels-like temperature is the perceived temperature, which may differ from the actual temperature due to
        factors like humidity and wind.

        :return feels_like: Feels-like temperature as a float.
        """
        return self.data.get('current', {}).get('feels_like', None)

    def get_current_pressure(self) -> int:
        """
        Returns the current atmospheric pressure from the response data.
        Pressure is measured in hPa (hectopascals).

        :return pressure: Current pressure as an integer.
        """
        return self.data.get('current', {}).get('pressure', None)

    def get_current_humidity(self) -> int | None:
        """
        Returns the current humidity in % from the response data.

        :return humidity: Current humidity as an integer or None.
        """
        return self.data.get('current', {}).get('humidity', None)

    def get_current_dew_point(self) -> float | None:
        """
        Returns the current dew point from the response data.

        :return dew_point: Current dew point as a float or None.
        """
        return self.data.get('current', {}).get('dew_point', None)

    def get_current_uvi(self) -> float | None:
        """
        Returns the current UV index from the response data.

        :return uvi: Current UV index as a float or None.
        """
        return self.data.get('current', {}).get('uvi', None)

    def get_current_clouds(self) -> int | None:
        """
        Returns the current cloudiness in % from the response data.

        :return clouds: Current cloudiness as an integer or None.
        """
        return self.data.get('current', {}).get('clouds', None)

    def get_current_visibility(self) -> int | None:
        """
        Returns the current visibility in km from the response data.

        :return visibility: Current visibility as an integer or None.
        """
        return self.data.get('current', {}).get('visibility', None)

    def get_current_wind_speed(self) -> float | None:
        """
        Returns the current wind speed from the response data.
        Wind speed is typically measured in meters per second (m/s), but can be converted to miles per hour (mph).

        :return wind_speed: Current wind speed as a float or None.
        """
        return self.data.get('current', {}).get('wind_speed', None)

    def get_current_wind_deg(self) -> int | None:
        """
        Returns the current wind direction in degrees from the response data.

        :return wind_deg: Current wind direction as an integer or None.
        """
        return self.data.get('current', {}).get('wind_deg', None)

    def get_current_wind_gust(self) -> float | None:
        """
        Returns the current wind gust speed from the response data.

        :return wind_gust: Current wind gust as a float or None.
        """
        return self.data.get('current', {}).get('wind_gust', None)

    def get_current_weather_id(self) -> int:
        """
        Returns the current weather condition ID from the response data.

        :return weather_id: Weather condition ID as an integer.
        """
        return self.data.get('current', {}).get('weather', [{}])[0].get('id', -1)

    def get_current_weather_main(self) -> str | None:
        """
        Returns the current weather main description from the response data.

        :return weather_main: Weather main as a string or None.
        """
        return self.data.get('current', {}).get('weather', [{}])[0].get('main', None)

    def get_current_weather_description(self) -> str | None:
        """
        Returns the current weather description from the response data.

        :return weather_description: Weather description as a string or None.
        """
        return self.data.get('current', {}).get('weather', [{}])[0].get('description', None)

    def get_current_weather_icon(self) -> str | None:
        """
        Returns the current weather icon code from the response data.

        :return weather_icon: Weather icon code as a string or None.
        """
        return self.data.get('current', {}).get('weather', [{}])[0].get('icon', None)

    def get_current_rain(self) -> float | None:
        """
        Returns the current rain volume from the response data.
        Rain volume is typically measured in mm (millimeters).

        :return rain: Current rain volume as a float or None.
        """
        return self.data.get('current', {}).get('rain', {}).get('1h', None)

    def get_current_snow(self) -> float | None:
        """
        Returns the current snow volume from the response data.
        Snow volume is typically measured in mm (millimeters).

        :return snow: Current snow volume as a float or None.
        """
        return self.data.get('current', {}).get('snow', {}).get('1h', None)

    def get_minutely_times(self) -> list[int | None]:
        """
        Returns a list of timestamps for each minutely forecast entry.

        :return minutely_times: List of timestamps (integers).
        """
        return [minute.get('dt', None) for minute in self.data.get('minutely', [])]

    def get_minutely_precipitation(self) -> list[float | None]:
        """
        Returns a list of precipitation values for each minutely forecast entry.

        :return minutely_precipitation: List of precipitation values (floats).
        """
        return [minute.get('precipitation', None) for minute in self.data.get('minutely', [])]

    def get_hourly_times(self) -> list[int | None]:
        """
        Returns a list of timestamps for each hourly forecast entry.

        :return hourly_times: List of timestamps (integers).
        """
        return [hour.get('dt', None) for hour in self.data.get('hourly', [])]

    def get_hourly_temp(self) -> list[float | None]:
        """
        Returns a list of temperatures for each hourly forecast entry.

        :return hourly_temp: List of temperatures (floats).
        """
        return [hour.get('temp', None) for hour in self.data.get('hourly', [])]

    def get_hourly_feels_like(self) -> list[float | None]:
        """
        Returns a list of feels-like temperatures for each hourly forecast entry.

        :return hourly_feels_like: List of feels-like temperatures (floats).
        """
        return [hour.get('feels_like', None) for hour in self.data.get('hourly', [])]

    def get_hourly_pressure(self) -> list[int | None]:
        """
        Returns a list of atmospheric pressures for each hourly forecast entry.

        :return hourly_pressure: List of pressures (integers).
        """
        return [hour.get('pressure', None) for hour in self.data.get('hourly', [])]

    def get_hourly_humidity(self) -> list[int | None]:
        """
        Returns a list of humidity values for each hourly forecast entry.

        :return hourly_humidity: List of humidity values (integers).
        """
        return [hour.get('humidity', None) for hour in self.data.get('hourly', [])]

    def get_hourly_dew_point(self) -> list[float | None]:
        """
        Returns a list of dew point values for each hourly forecast entry.

        :return hourly_dew_point: List of dew point values (floats).
        """
        return [hour.get('dew_point', None) for hour in self.data.get('hourly', [])]

    def get_hourly_uvi(self) -> list[float | None]:
        """
        Returns a list of UV index values for each hourly forecast entry.

        :return hourly_uvi: List of UV index values (floats).
        """
        return [hour.get('uvi', None) for hour in self.data.get('hourly', [])]

    def get_hourly_clouds(self) -> list[int | None]:
        """
        Returns a list of cloudiness values for each hourly forecast entry.

        :return hourly_clouds: List of cloudiness values (integers).
        """
        return [hour.get('clouds', None) for hour in self.data.get('hourly', [])]

    def get_hourly_visibility(self) -> list[int | None]:
        """
        Returns a list of visibility values for each hourly forecast entry.

        :return hourly_visibility: List of visibility values (integers).
        """
        return [hour.get('visibility', None) for hour in self.data.get('hourly', [])]

    def get_hourly_wind_speed(self) -> list[float | None]:
        """
        Returns a list of wind speed values for each hourly forecast entry.

        :return hourly_wind_speed: List of wind speed values (floats).
        """
        return [hour.get('wind_speed', None) for hour in self.data.get('hourly', [])]

    def get_hourly_wind_deg(self) -> list[int | None]:
        """
        Returns a list of wind direction values for each hourly forecast entry.

        :return hourly_wind_deg: List of wind direction values (integers).
        """
        return [hour.get('wind_deg', None) for hour in self.data.get('hourly', [])]

    def get_hourly_wind_gust(self) -> list[float | None]:
        """
        Returns a list of wind gust values for each hourly forecast entry.

        :return hourly_wind_gust: List of wind gust values (floats).
        """
        return [hour.get('wind_gust', None) for hour in self.data.get('hourly', [])]

    def get_hourly_pop(self) -> list[float | None]:
        """
        Returns a list of probability of precipitation values for each hourly forecast entry.

        :return hourly_pop: List of probability of precipitation values (floats).
        """
        return [hour.get('pop', None) for hour in self.data.get('hourly', [])]

    def get_hourly_rain(self) -> list[float | None]:
        """
        Returns a list of rain volume values for each hourly forecast entry.

        :return hourly_rain: List of rain volume values (floats).
        """
        return [hour.get('rain', None) for hour in self.data.get('hourly', [])]

    def get_hourly_snow(self) -> list[float | None]:
        """
        Returns a list of snow volume values for each hourly forecast entry.

        :return hourly_snow: List of snow volume values (floats).
        """
        return [hour.get('snow', None) for hour in self.data.get('hourly', [])]

    def get_hourly_weather_id(self) -> list[int]:
        """
        Returns a list of weather condition IDs for each hourly forecast entry.

        :return hourly_weather_id: List of weather condition IDs (integers).
        """
        return [hour.get('weather', [{}])[0].get('id', -1) for hour in self.data.get('hourly', [])]

    def get_hourly_weather_main(self) -> list[str | None]:
        """
        Returns a list of weather main descriptions for each hourly forecast entry.

        :return hourly_weather_main: List of weather main descriptions (strings).
        """
        return [hour.get('weather', [{}])[0].get('main', None) for hour in self.data.get('hourly', [])]

    def get_hourly_weather_description(self) -> list[str | None]:
        """
        Returns a list of weather descriptions for each hourly forecast entry.

        :return hourly_weather_description: List of weather descriptions (strings).
        """
        return [hour.get('weather', [{}])[0].get('description', None) for hour in self.data.get('hourly', [])]

    def get_hourly_weather_icon(self) -> list[str | None]:
        """
        Returns a list of weather icon codes for each hourly forecast entry.

        :return hourly_weather_icon: List of weather icon codes (strings).
        """
        return [hour.get('weather', [{}])[0].get('icon', None) for hour in self.data.get('hourly', [])]

    def get_daily_times(self) -> list[int | None]:
        """
        Returns a list of timestamps for each daily forecast entry.

        :return daily_times: List of timestamps (integers).
        """
        return [day.get('dt', None) for day in self.data.get('daily', [])]

    def get_daily_sunrise(self) -> list[int | None]:
        """
        Returns a list of sunrise times for each daily forecast entry.

        :return daily_sunrise: List of sunrise times (integers).
        """
        return [day.get('sunrise', None) for day in self.data.get('daily', [])]

    def get_daily_sunset(self) -> list[int | None]:
        """
        Returns a list of sunset times for each daily forecast entry.

        :return daily_sunset: List of sunset times (integers).
        """
        return [day.get('sunset', None) for day in self.data.get('daily', [])]

    def get_daily_moonrise(self) -> list[int | None]:
        """
        Returns a list of moonrise times for each daily forecast entry.

        :return daily_moonrise: List of moonrise times (integers).
        """
        return [day.get('moonrise', None) for day in self.data.get('daily', [])]

    def get_daily_moonset(self) -> list[int | None]:
        """
        Returns a list of moonset times for each daily forecast entry.

        :return daily_moonset: List of moonset times (integers).
        """
        return [day.get('moonset', None) for day in self.data.get('daily', [])]

    def get_daily_moon_phase(self) -> list[float | None]:
        """
        Returns a list of moon phase values for each daily forecast entry.

        :return daily_moon_phase: List of moon phase values (floats).
        """
        return [day.get('moon_phase', None) for day in self.data.get('daily', [])]

    def get_daily_summary(self) -> list[str | None]:
        """
        Returns a list of summary strings for each daily forecast entry.

        :return daily_summary: List of summary strings (strings).
        """
        return [day.get('summary', None) for day in self.data.get('daily', [])]

    def get_daily_temp_day(self) -> list[float | None]:
        """
        Returns a list of daytime temperatures for each daily forecast entry.

        :return daily_temp_day: List of daytime temperatures (floats).
        """
        return [day.get('temp', {}).get('day', None) for day in self.data.get('daily', [])]

    def get_daily_temp_min(self) -> list[float | None]:
        """
        Returns a list of minimum temperatures for each daily forecast entry.

        :return daily_temp_min: List of minimum temperatures (floats).
        """
        return [day.get('temp', {}).get('min', None) for day in self.data.get('daily', [])]

    def get_daily_temp_max(self) -> list[float | None]:
        """
        Returns a list of maximum temperatures for each daily forecast entry.

        :return daily_temp_max: List of maximum temperatures (floats).
        """
        return [day.get('temp', {}).get('max', None) for day in self.data.get('daily', [])]

    def get_daily_temp_night(self) -> list[float | None]:
        """
        Returns a list of nighttime temperatures for each daily forecast entry.

        :return daily_temp_night: List of nighttime temperatures (floats).
        """
        return [day.get('temp', {}).get('night', None) for day in self.data.get('daily', [])]

    def get_daily_temp_eve(self) -> list[float | None]:
        """
        Returns a list of evening temperatures for each daily forecast entry.

        :return daily_temp_eve: List of evening temperatures (floats).
        """
        return [day.get('temp', {}).get('eve', None) for day in self.data.get('daily', [])]

    def get_daily_temp_morning(self) -> list[float | None]:
        """
        Returns a list of morning temperatures for each daily forecast entry.

        :return daily_temp_morning: List of morning temperatures (floats).
        """
        return [day.get('temp', {}).get('morn', None) for day in self.data.get('daily', [])]

    def get_daily_feels_like_day(self) -> list[float | None]:
        """
        Returns a list of daytime feels-like temperatures for each daily forecast entry.

        :return daily_feels_like_day: List of daytime feels-like temperatures (floats).
        """
        return [day.get('feels_like', {}).get('day', None) for day in self.data.get('daily', [])]

    def get_daily_feels_like_night(self) -> list[float | None]:
        """
        Returns a list of nighttime feels-like temperatures for each daily forecast entry.

        :return daily_feels_like_night: List of nighttime feels-like temperatures (floats).
        """
        return [day.get('feels_like', {}).get('night', None) for day in self.data.get('daily', [])]

    def get_daily_feels_like_eve(self) -> list[float | None]:
        """
        Returns a list of evening feels-like temperatures for each daily forecast entry.

        :return daily_feels_like_eve: List of evening feels-like temperatures (floats).
        """
        return [day.get('feels_like', {}).get('eve', None) for day in self.data.get('daily', [])]

    def get_daily_feels_like_morning(self) -> list[float | None]:
        """
        Returns a list of morning feels-like temperatures for each daily forecast entry.

        :return daily_feels_like_morning: List of morning feels-like temperatures (floats).
        """
        return [day.get('feels_like', {}).get('morn', None) for day in self.data.get('daily', [])]

    def get_daily_pressure(self) -> list[int | None]:
        """
        Returns a list of atmospheric pressures for each daily forecast entry.

        :return daily_pressure: List of pressures (integers).
        """
        return [day.get('pressure', None) for day in self.data.get('daily', [])]

    def get_daily_humidity(self) -> list[int | None]:
        """
        Returns a list of humidity values for each daily forecast entry.

        :return daily_humidity: List of humidity values (integers).
        """
        return [day.get('humidity', None) for day in self.data.get('daily', [])]

    def get_daily_dew_point(self) -> list[float | None]:
        """
        Returns a list of dew point values for each daily forecast entry.

        :return daily_dew_point: List of dew point values (floats).
        """
        return [day.get('dew_point', None) for day in self.data.get('daily', [])]

    def get_daily_wind_speed(self) -> list[float | None]:
        """
        Returns a list of wind speed values for each daily forecast entry.

        :return daily_wind_speed: List of wind speed values (floats).
        """
        return [day.get('wind_speed', None) for day in self.data.get('daily', [])]

    def get_daily_wind_deg(self) -> list[int | None]:
        """
        Returns a list of wind direction values for each daily forecast entry.

        :return daily_wind_deg: List of wind direction values (integers).
        """
        return [day.get('wind_deg', None) for day in self.data.get('daily', [])]

    def get_daily_wind_gust(self) -> list[float | None]:
        """
        Returns a list of wind gust values for each daily forecast entry.

        :return daily_wind_gust: List of wind gust values (floats).
        """
        return [day.get('wind_gust', None) for day in self.data.get('daily', [])]

    def get_daily_weather_id(self) -> list[int]:
        """
        Returns a list of weather condition IDs for each daily forecast entry.

        :return daily_weather_id: List of weather condition IDs (integers).
        """
        return [day.get('weather', [{}])[0].get('id', -1) for day in self.data.get('daily', [])]

    def get_daily_weather_main(self) -> list[str | None]:
        """
        Returns a list of weather main descriptions for each daily forecast entry.

        :return daily_weather_main: List of weather main descriptions (strings).
        """
        return [day.get('weather', [{}])[0].get('main', None) for day in self.data.get('daily', [])]

    def get_daily_weather_description(self) -> list[str | None]:
        """
        Returns a list of weather descriptions for each daily forecast entry.

        :return daily_weather_description: List of weather descriptions (strings).
        """
        return [day.get('weather', [{}])[0].get('description', None) for day in self.data.get('daily', [])]

    def get_daily_weather_icon(self) -> list[str | None]:
        """
        Returns a list of weather icon codes for each daily forecast entry.

        :return daily_weather_icon: List of weather icon codes (strings).
        """
        return [day.get('weather', [{}])[0].get('icon', None) for day in self.data.get('daily', [])]

    def get_daily_pop(self) -> list[float | None]:
        """
        Returns a list of probability of precipitation values for each daily forecast entry.

        :return daily_pop: List of probability of precipitation values (floats).
        """
        return [day.get('pop', None) for day in self.data.get('daily', [])]

    def get_daily_rain(self) -> list[float | None]:
        """
        Returns a list of rain volume values for each daily forecast entry.

        :return daily_rain: List of rain volume values (floats).
        """
        return [day.get('rain', None) for day in self.data.get('daily', [])]

    def get_daily_uvi(self) -> list[float | None]:
        """
        Returns a list of UV index values for each daily forecast entry.

        :return daily_uvi: List of UV index values (floats).
        """
        return [day.get('uvi', None) for day in self.data.get('daily', [])]

    def get_daily_clouds(self) -> list[int | None]:
        """
        Returns a list of cloudiness values for each daily forecast entry.

        :return daily_clouds: List of cloudiness values (integers).
        """
        return [day.get('clouds', None) for day in self.data.get('daily', [])]

    def get_daily_snow(self) -> list[float | None]:
        """
        Returns a list of snow volume values for each daily forecast entry.

        :return daily_snow: List of snow volume values (floats).
        """
        return [day.get('snow', None) for day in self.data.get('daily', [])]

    def get_daily_weather_id(self) -> list[int]:
        """
        Returns a list of weather condition IDs for each daily forecast entry.

        :return daily_weather_id: List of weather condition IDs (integers).
        """
        return [day.get('weather', [{}])[0].get('id', -1) for day in self.data.get('daily', [])]

    def get_daily_weather_main(self) -> list[str | None]:
        """
        Returns a list of weather main descriptions for each daily forecast entry.

        :return daily_weather_main: List of weather main descriptions (strings).
        """
        return [day.get('weather', [{}])[0].get('main', None) for day in self.data.get('daily', [])]

    def get_daily_weather_description(self) -> list[str | None]:
        """
        Returns a list of weather descriptions for each daily forecast entry.

        :return daily_weather_description: List of weather descriptions (strings).
        """
        return [day.get('weather', [{}])[0].get('description', None) for day in self.data.get('daily', [])]

    def get_daily_weather_icon(self) -> list[str | None]:
        """
        Returns a list of weather icon codes for each daily forecast entry.

        :return daily_weather_icon: List of weather icon codes (strings).
        """
        return [day.get('weather', [{}])[0].get('icon', None) for day in self.data.get('daily', [])]

    def get_alerts(self) -> list[OpenWeatherAlert]:
        """
        Returns a list of alerts from the response data.

        :return alerts: List of OpenWeatherAlert objects.
        """
        alerts_data = self.data.get('alerts', [])
        return [OpenWeatherAlert(alert) for alert in alerts_data] if alerts_data else []

class OneCallAggregationResponse:
    """A class to handle the aggregation response from the OpenWeather One Call API."""

    def __init__(self, data):
        """ Initializes the OneCallAggregationResponse with the provided data.

        :param data: A dictionary containing the aggregation response data from the One Call API.
        """
        self.data = data

    def get_latitude(self) -> float:
        """
        Returns the latitude from the aggregation response data.
        Latitude will be a value between -90 and 90.

        :return latitude: Latitude as a float.
        """
        return self.data.get('lat', 0.0)

    def get_longitude(self) -> float:
        """
        Returns the longitude from the aggregation response data.
        Longitude will be a value between -180 and 180.

        :return longitude: Longitude as a float.
        """
        return self.data.get('lon', 0.0)

    def get_timezone(self) -> str:
        """
        Returns the timezone from the aggregation response data.
        Timezone is a string representing the timezone of the location.
        Example: '+00:00'

        :return timezone: Timezone as a string.
        """
        return self.data.get('timezone', '+00:00')

    def get_date(self) -> str:
        """
        Returns the date from the aggregation response data.
        Date is a string in the format 'YYYY-MM-DD'.

        :return date: Date as a string.
        """
        return self.data.get('date', '1970-01-01')

    def get_units(self) -> str:
        """
        Returns the units used in the aggregation response data.
        Units can be 'metric', 'imperial', or 'standard'.

        :return units: Units as a string.
        """
        return self.data.get('units', 'standard')

    def get_cloud_cover_afternoon(self) -> int:
        """
        Returns a list of cloud cover values for the afternoon period of each daily forecast entry.

        :return cloud_cover_afternoon: The cloud coverage.
        """
        return self.data.get('cloud_cover', {}).get('afternoon', -1)

    def get_humidity_afternoon(self) -> int:
        """
        Returns a list of humidity values for the afternoon period of each daily forecast entry.

        :return humidity_afternoon: The humidity.
        """
        return self.data.get('humidity', {}).get('afternoon', -1)

    def get_total_precipitation(self) -> float:
        """
        Returns a list of total precipitation values for each daily forecast entry.

        :return total_precipitation: The total precipitation.
        """
        return self.data.get('precipitation', {}).get('total', -1.0)

    def get_temperature_min(self) -> float:
        """
        Returns a list of minimum temperatures for each daily forecast entry.

        :return temperature_min: The minimum temperature.
        """
        return self.data.get('temperature', {}).get('min', -1.0)

    def get_temperature_max(self) -> float:
        """
        Returns a list of maximum temperatures for each daily forecast entry.

        :return temperature_max: The maximum themperature.
        """
        return self.data.get('temperature', {}).get('max', -1.0)

    def get_temperature_afternoon(self) -> float:
        """
        Returns a list of afternoon temperatures for each daily forecast entry.

        :return temperature_afternoon: The temperature in the afternoon.
        """
        return self.data.get('temperature', {}).get('afternoon', -1.0)

    def get_temperature_morning(self) -> float:
        """
        Returns a list of morning temperatures for each daily forecast entry.

        :return temperature_morning: The temperature in the morning.
        """
        return self.data.get('temperature', {}).get('morning', -1.0)

    def get_temperature_night(self) -> float:
        """
        Returns a list of nighttime temperatures for each daily forecast entry.

        :return temperature_night: The temperature at night.
        """
        return self.data.get('temperature', {}).get('night', -1.0)

    def get_temperature_evening(self) -> float:
        """
        Returns a list of evening temperatures for each daily forecast entry.

        :return temperature_evening: The temperature in the evening.
        """
        return self.data.get('temperature', {}).get('evening', -1.0)

    def get_pressure_afternoon(self) -> int:
        """
        Returns a list of atmospheric pressures for each daily forecast entry.

        :return pressure_afternoon: The pressure for the afternoon.
        """
        return self.data.get('pressure', {}).get('afternoon', -1)

    def get_wind_max_speed(self) -> float:
        """
        Returns a list of maximum wind speeds for each daily forecast entry.

        :return wind_max_speed: The maximum wind speed.
        """
        return self.data.get('wind', {}).get('max', {}).get('speed', -1.0)

    def get_wind_max_direction(self) -> int:
        """
        Returns a list of maximum wind directions for each daily forecast entry.

        :return wind_max_direction: The maximum wind direction.
        """
        return self.data.get('wind', {}).get('max', {}).get('direction', -1)

class OneCallTimestampedResponse:
    """A class to handle the timestamped response from the OpenWeather One Call API."""

    def __init__(self, data):
        """ Initializes the OneCallTimestampedResponse with the provided data.

        :param data: A dictionary containing the timestamped response data from the One Call API.
        """
        self.data = data

    def get_latitude(self) -> float:
        """
        Returns the latitude of the location from the response data.

        :return latitude: Latitude as a float.
        """
        return self.data.get('lat', 0.0)

    def get_longitude(self) -> float:
        """
        Returns the longitude of the location from the response data.

        :return longitude: Longitude as a float.
        """
        return self.data.get('lon', 0.0)

    def get_timezone(self) -> str:
        """
        Returns the timezone of the location from the response data.

        :return timezone: Timezone as a string.
        """
        return self.data.get('timezone', 'UTC')

    def get_timezone_offset(self) -> int:
        """
        Returns the timezone offset in seconds from the response data.

        :return timezone_offset: Timezone offset as an integer.
        """
        return self.data.get('timezone_offset', 0)

    def get_time(self) -> int:
        """
        Returns the time of the response data.

        Returns:
            int: The time of the response data as a timestamp.
        """
        return self.data.get('data', [{}])[0].get('dt', -1)

    def get_sunrise(self) -> int:
        """
        Returns the sunrise time from the response data.

        Returns:
            int: The sunrise time as a timestamp.
        """
        return self.data.get('data', [{}])[0].get('sunrise', -1)

    def get_sunset(self) -> int:
        """
        Returns the sunset time from the response data.

        Returns:
            int: The sunset time as a timestamp.
        """
        return self.data.get('data', [{}])[0].get('sunset', -1)

    def get_temperature(self) -> float:
        """
        Returns the temperature from the response data.

        Returns:
            float: The temperature as a float.
        """
        return self.data.get('data', [{}])[0].get('temp', -1.0)

    def get_feels_like(self) -> float:
        """
        Returns the feels-like temperature from the response data.

        Returns:
            float: The feels-like temperature as a float.
        """
        return self.data.get('data', [{}])[0].get('feels_like', -1.0)

    def get_pressure(self) -> int:
        """
        Returns the atmospheric pressure from the response data.

        Returns:
            int: The atmospheric pressure as an integer.
        """
        return self.data.get('data', [{}])[0].get('pressure', -1)

    def get_humidity(self) -> int:
        """
        Returns the humidity from the response data.

        Returns:
            int: The humidity as an integer.
        """
        return self.data.get('data', [{}])[0].get('humidity', -1)

    def get_dew_point(self) -> float:
        """
        Returns the dew point from the response data.

        Returns:
            float: The dew point as a float.
        """
        return self.data.get('data', [{}])[0].get('dew_point', -1.0)

    def get_uvi(self) -> float:
        """
        Returns the UV index from the response data.

        Returns:
            float: The UV index as a float.
        """
        return self.data.get('data', [{}])[0].get('uvi', -1.0)

    def get_clouds(self) -> int:
        """
        Returns the cloudiness from the response data.

        Returns:
            int: The cloudiness as an integer.
        """
        return self.data.get('data', [{}])[0].get('clouds', -1)

    def get_visibility(self) -> int:
        """
        Returns the visibility from the response data.

        Returns:
            int: The visibility as an integer.
        """
        return self.data.get('data', [{}])[0].get('visibility', -1)

    def get_wind_speed(self) -> float:
        """
        Returns the wind speed from the response data.

        Returns:
            float: The wind speed as a float.
        """
        return self.data.get('data', [{}])[0].get('wind_speed', -1.0)

    def get_wind_deg(self) -> int:
        """
        Returns the wind direction in degrees from the response data.

        Returns:
            int: The wind direction as an integer.
        """
        return self.data.get('data', [{}])[0].get('wind_deg', -1)

    def get_weather_id(self) -> int:
        """
        Returns the weather condition ID from the response data.

        Returns:
            int: The weather condition ID as an integer.
        """
        return self.data.get('data', [{}])[0].get('weather', [{}])[0].get('id', -1)

    def get_weather_main(self) -> str | None:
        """
        Returns the main weather description from the response data.

        Returns:
            str | None: The main weather description as a string or None.
        """
        return self.data.get('data', [{}])[0].get('weather', [{}])[0].get('main', None)

    def get_weather_description(self) -> str | None:
        """
        Returns the weather description from the response data.

        Returns:
            str | None: The weather description as a string or None.
        """
        return self.data.get('data', [{}])[0].get('weather', [{}])[0].get('description', None)

    def get_weather_icon(self) -> str | None:
        """
        Returns the weather icon code from the response data.

        Returns:
            str | None: The weather icon code as a string or None.
        """
        return self.data.get('data', [{}])[0].get('weather', [{}])[0].get('icon', None)

class CurrentWeatherResponse:
    """A class to handle the response from the OpenWeather Current Weather API."""
    def __init__(self, data: dict | str, mode: Literal["json", "xml"]='json'):
        """
        Initializes the CurrentWeatherResponse with the provided data.

        Depending on the mode, the available data may vary as some fields are not present in XML or HTML responses, while other fields are not present in JSON format.

        :param data: A dictionary containing the response data from the Current Weather API.
        :param mode: The mode of the response, can be 'json', or 'xml', Defaults to 'json'.
        """
        self.data = data
        self.mode = mode

    def get_latitude(self) -> float:
        """
        Returns the latitude from the response data.
        Latitude will be a value between -90 and 90.

        :return latitude: Latitude as a float.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                coord = city.find('coord')
                if coord is not None:
                    return float(coord.get('lat', 0.0))
            return 0.0
        else:
            return self.data.get('coord', {}).get('lat', 0.0)

    def get_longitude(self) -> float:
        """
        Returns the longitude from the response data.
        Longitude will be a value between -180 and 180.

        :return longitude: Longitude as a float.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                coord = city.find('coord')
                if coord is not None:
                    return float(coord.get('lon', 0.0))
            return 0.0
        else:
            return self.data.get('coord', {}).get('lon', 0.0)

    def get_weather_id(self) -> int:
        """
        Returns the weather condition ID from the response data.

        :return weather_id: Weather condition ID as an integer.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            weather = root.find('weather')
            if weather is not None:
                return int(weather.get('number', -1))
            return None
        else:
            return self.data.get('weather', [{}])[0].get('id', -1)

    def get_weather_main(self) -> str | None:
        """
        Returns the main weather description from the response data.

        Returns None if the mode is 'xml' since the main description is not available in those formats.

        :return weather_main: Weather main description as a string or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('weather', [{}])[0].get('main', None)

    def get_weather_description(self) -> str | None:
        """
        Returns the weather description from the response data.

        :return weather_description: Weather description as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            weather = root.find('weather')
            if weather is not None:
                return weather.get('value', None)
            return None
        else:
            return self.data.get('weather', [{}])[0].get('description', None)

    def get_weather_icon(self) -> str | None:
        """
        Returns the weather icon code from the response data.

        :return weather_icon: Weather icon code as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            weather = root.find('weather')
            if weather is not None:
                return weather.get('icon', None)
            return None
        else:
            return self.data.get('weather', [{}])[0].get('icon', None)

    def get_base(self) -> str | None:
        """
        Returns the base of the weather data from the response data.

        Returns None if the mode is 'xml' since the base is not available in those formats.

        :return base: Base as a string or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('base', None)

    def get_temparature(self) -> float | None:
        """
        Returns the current temperature from the response data.
        Temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return temperature: Current temperature as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            temperature = root.find('temperature')
            if temperature is not None:
                return float(temperature.get('value', 0.0))
            return None
        else:
            return self.data.get('main', {}).get('temp', None)

    def get_temperature_unit(self) -> str | None:
        """
        Returns the unit of the temperature from the response data.
        The unit is typically 'metric' for Celsius or 'imperial' for Fahrenheit.

        Returns None if the mode is 'json' since the unit is not available in that format.

        :return temperature_unit: Temperature unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            temperature = root.find('temperature')
            if temperature is not None:
                return temperature.get('unit', None)
            return None
        else:
            return None

    def get_feels_like(self) -> float | None:
        """
        Returns the feels-like temperature from the response data.
        Feels-like temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return feels_like: Feels-like temperature as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            feels_like = root.find('feels_like')
            if feels_like is not None:
                return float(feels_like.get('value', 0.0))
            return None
        else:
            return self.data.get('main', {}).get('feels_like', None)

    def get_feels_like_unit(self) -> str | None:
        """
        Returns the unit of the feels-like temperature from the response data.
        The unit is typically 'metric' for Celsius or 'imperial' for Fahrenheit.

        Returns None if the mode is 'json' since the unit is not available in that format.

        :return feels_like_unit: Feels-like temperature unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            feels_like = root.find('feels_like')
            if feels_like is not None:
                return feels_like.get('unit', None)
            return None
        else:
            return None

    def get_pressure(self) -> int | None:
        """
        Returns the atmospheric pressure from the response data.
        Pressure is typically measured in hPa (hectopascals).

        :return pressure: Atmospheric pressure as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            pressure = root.find('pressure')
            if pressure is not None:
                return int(pressure.get('value', 0))
            return None
        else:
            return self.data.get('main', {}).get('pressure', None)

    def get_pressure_unit(self) -> str | None:
        """
        Returns the unit of the atmospheric pressure from the response data.
        The unit is typically 'hPa' (hectopascals).

        Returns None if the mode is 'json' since the unit is not available in that format.

        :return pressure_unit: Atmospheric pressure unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            pressure = root.find('pressure')
            if pressure is not None:
                return pressure.get('unit', None)
            return None
        else:
            return None

    def get_humidity(self) -> int | None:
        """
        Returns the humidity from the response data.
        Humidity is typically measured as a percentage (0-100%).

        :return humidity: Humidity as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            humidity = root.find('humidity')
            if humidity is not None:
                return int(humidity.get('value', 0))
            return None
        else:
            return self.data.get('main', {}).get('humidity', None)

    def get_humidity_unit(self) -> str | None:
        """
        Returns the unit of the humidity from the response data.
        The unit is typically 'percent' for percentage.

        Returns None if the mode is 'json' since the unit is not available in that format.

        :return humidity_unit: Humidity unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            humidity = root.find('humidity')
            if humidity is not None:
                return humidity.get('unit', None)
            return None
        else:
            return None

    def get_temperature_min(self) -> float | None:
        """
        Returns the minimum temperature from the response data.
        Minimum temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return min_temperature: Minimum temperature as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            temperature = root.find('temperature')
            if temperature is not None:
                return float(temperature.get('min', 0.0))
            return None
        else:
            return self.data.get('main', {}).get('temp_min', None)

    def get_temperature_max(self) -> float | None:
        """
        Returns the maximum temperature from the response data.
        Maximum temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return max_temperature: Maximum temperature as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            temperature = root.find('temperature')
            if temperature is not None:
                return float(temperature.get('max', 0.0))
            return None
        else:
            return self.data.get('main', {}).get('temp_max', None)

    def get_sea_level_pressure(self) -> int | None:
        """
        Returns the sea level pressure from the response data.
        Sea level pressure is typically measured in hPa (hectopascals).

        Returns None if the mode is 'xml' since sea level pressure is not available in those formats.

        :return sea_level_pressure: Sea level pressure as an integer or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('main', {}).get('sea_level', None)

    def get_ground_level_pressure(self) -> int | None:
        """
        Returns the ground level pressure from the response data.
        Ground level pressure is typically measured in hPa (hectopascals).

        Returns None if the mode is 'xml' since ground level pressure is not available in those formats.

        :return ground_level_pressure: Ground level pressure as an integer or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('main', {}).get('grnd_level', None)

    def get_visibility(self) -> int | None:
        """
        Returns the visibility from the response data.
        Visibility is typically measured in meters.

        The maximum visibility is 10,000 meters, and values above this are often capped at 10,000.

        :return visibility: Visibility as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            visibility = root.find('visibility')
            if visibility is not None:
                return int(visibility.get('value', 0))
            return None
        else:
            return self.data.get('visibility', None)

    def get_wind_speed(self) -> float | None:
        """
        Returns the wind speed from the response data.
        Wind speed is typically measured in meters per second (m/s).

        :return wind_speed: Wind speed as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind = root.find('wind')
            if wind is not None:
                speed = wind.find('speed')
                if speed is not None:
                    return float(speed.get('value', 0.0))
            return None
        else:
            return self.data.get('wind', {}).get('speed', None)

    def get_wind_speed_unit(self) -> str | None:
        """
        Returns the unit of the wind speed from the response data.
        The unit is typically 'm/s' (meters per second).

        Returns None if the mode is 'json' since the unit is not available in that format.

        :return wind_speed_unit: Wind speed unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind = root.find('wind')
            if wind is not None:
                speed = wind.find('speed')
                if speed is not None:
                    return speed.get('unit', None)
            return None
        else:
            return None

    def get_wind_speed_name(self) -> str | None:
        """
        Returns the name of the wind speed from the response data.
        The name is typically a string representing the wind speed category.

        Returns None if the mode is 'json' since the name is not available in that format.

        :return wind_speed_name: Wind speed name as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind = root.find('wind')
            if wind is not None:
                speed = wind.find('speed')
                if speed is not None:
                    return speed.get('name', None)
            return None
        else:
            return None

    def get_wind_deg(self) -> int | None:
        """
        Returns the wind direction from the response data.
        Wind direction is typically measured in degrees (0-360).

        :return wind_deg: Wind direction as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind = root.find('wind')
            if wind is not None:
                direction = wind.find('direction')
                if direction is not None:
                    return int(direction.get('value', 0))
            return None
        else:
            return self.data.get('wind', {}).get('deg', None)

    def get_wind_direction(self) -> str | None:
        """
        Returns the wind direction as a string from the response data.
        The direction is typically represented as a cardinal direction (e.g., 'N', 'NE', 'E', etc.).

        Returns None if the mode is 'json' since the direction is not available in that format.

        :return wind_direction: Wind direction as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind = root.find('wind')
            if wind is not None:
                direction = wind.find('direction')
                if direction is not None:
                    return direction.get('name', None)
            return None
        else:
            return None

    def get_wind_direction_full(self) -> str | None:
        """
        Returns the full wind direction as a string from the response data.
        The full direction is typically represented as a more descriptive string (e.g., 'North', 'Northeast', etc.).

        Returns None if the mode is 'json' since the full direction is not available in that format.

        :return wind_direction_full: Full wind direction as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind = root.find('wind')
            if wind is not None:
                direction = wind.find('direction')
                if direction is not None:
                    return direction.get('name', None)
            return None
        else:
            return None

    def get_wind_gust(self) -> float | None:
        """
        Returns the wind gust speed from the response data.
        Wind gust speed is typically measured in meters per second (m/s).

        Returns None if the mode is 'xml' since wind gust speed is not available in those formats.

        :return wind_gust: Wind gust speed as a float or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('wind', {}).get('gust', None)

    def get_clouds(self) -> int | None:
        """
        Returns the cloudiness from the response data.
        Cloudiness is typically measured as a percentage (0-100%).

        :return clouds: Cloudiness as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            clouds = root.find('clouds')
            if clouds is not None:
                return int(clouds.get('value', 0))
            return None
        else:
            return self.data.get('clouds', {}).get('all', None)

    def get_clouds_name(self) -> str | None:
        """
        Returns the name of the cloudiness from the response data.
        The name is typically a string representing the cloudiness category.

        Returns None if the mode is 'json' since the name is not available in that format.

        :return clouds_name: Cloudiness name as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            clouds = root.find('clouds')
            if clouds is not None:
                return clouds.get('name', None)
            return None
        else:
            return None

    def get_rain(self) -> float | None:
        """
        Returns the rain volume from the response data.
        Rain volume is typically measured in millimeters/hour (mm/h).

        :return rain: Rain volume as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            precipitation = root.find('precipitation')
            if precipitation is not None:
                mode = precipitation.get('mode', 'no')
                if mode == 'no' or mode == 'snow':
                    return None
                elif mode == 'rain':
                    return float(precipitation.get('value', 0.0))
            return None
        else:
            return self.data.get('rain', {}).get('1h', None)

    def get_snow(self) -> float | None:
        """
        Returns the snow volume from the response data.
        Snow volume is typically measured in millimeters/hour (mm/h).

        :return snow: Snow volume as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            precipitation = root.find('precipitation')
            if precipitation is not None:
                mode = precipitation.get('mode', 'no')
                if mode == 'no' or mode == 'rain':
                    return None
                elif mode == 'snow':
                    return float(precipitation.get('value', 0.0))
            return None
        else:
            return self.data.get('snow', {}).get('1h', None)

    def get_time(self) -> int | None:
        """
        Returns the time of the weather data from the response data.
        The time is typically represented as a Unix timestamp (seconds since epoch).

        Returns None if the mode is 'xml' since time is not available in those formats.

        :return time: Time as an integer (Unix timestamp) or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('dt', None)

    def get_sys_type(self) -> int | None:
        """
        Returns the system type from the response data.
        The system type is typically an integer representing the type of data.

        Returns None if the mode is 'xml' since system type is not available in those formats.

        :return sys_type: System type as an integer or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('sys', {}).get('type', None)

    def get_sys_id(self) -> int | None:
        """
        Returns the system ID from the response data.
        The system ID is typically an integer representing the unique identifier of the system.

        Returns None if the mode is 'xml' since system ID is not available in those formats.

        :return sys_id: System ID as an integer or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('sys', {}).get('id', None)

    def get_sys_message(self) -> float | None:
        """
        Returns the system message from the response data.
        The system message is typically a float representing additional information about the system.

        Returns None if the mode is 'xml' since system message is not available in those formats.

        :return sys_message: System message as a float or None.
        """
        if self.mode == 'xml':
            return None
        else:
            return self.data.get('sys', {}).get('message', None)

    def get_country(self) -> str | None:
        """
        Returns the country code from the response data.
        The country code is typically a two-letter ISO 3166-1 alpha-2 code.

        Returns None if the mode is 'xml' since country code is not available in those formats.

        :return country: Country code as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                return city.get('country', None)
        else:
            return self.data.get('sys', {}).get('country', None)

    def get_sunrise(self) -> int | str| None:
        """
        Returns the sunrise time from the response data.
        Sunrise time is typically represented as a Unix timestamp (seconds since epoch).

        Sunrise will be a string in XML or HTML mode, while in JSON mode it will be an integer.

        :return sunrise: Sunrise time as an integer (Unix timestamp) or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                sun = city.find('sun')
                if sun is not None:
                    return sun.get('rise', None)
            return None
        else:
            return self.data.get('sys', {}).get('sunrise', None)

    def get_sunset(self) -> int | None:
        """
        Returns the sunset time from the response data.
        Sunset time is typically represented as a Unix timestamp (seconds since epoch).

        Sunset will be a string in XML or HTML mode, while in JSON mode it will be an integer.

        :return sunset: Sunset time as an integer (Unix timestamp) or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                sun = city.find('sun')
                if sun is not None:
                    return sun.get('set', None)
            return None
        else:
            return self.data.get('sys', {}).get('sunset', None)

    def get_timezone(self) -> int | None:
        """
        Returns the timezone offset from the response data.
        The timezone offset is typically represented in seconds from UTC.

        :return timezone: Timezone offset as an integer (seconds) or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                return int(city.get('timezone', 0))
            return None
        else:
            return self.data.get('timezone', None)

    def get_city_id(self) -> int | None:
        """
        Returns the city ID from the response data.
        The city ID is typically an integer representing the unique identifier of the city.

        :return city_id: City ID as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                return int(city.get('id', 0))
            return None
        else:
            return self.data.get('id', None)

    def get_city_name(self) -> str | None:
        """
        Returns the city name from the response data.
        The city name is typically a string representing the name of the city.

        :return city_name: City name as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            city = root.find('city')
            if city is not None:
                return city.get('name', None)
            return None
        else:
            return self.data.get('name', None)

    def get_lastupdate(self) -> str | None:
        """
        Returns the last update time from the response data.
        The last update is a string in the format 'YYYY-MM-DD HH:MM:SS'.

        Returns None if the mode is 'json' since last update time is not available in those formats.

        :return last_update: Last update time as an integer (Unix timestamp) or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            lastupdate = root.find('lastupdate')
            if lastupdate is not None:
                return lastupdate.get('value', None)
            return None
        else:
            return None

class FiveDayForecastResponse:
    """A class to handle the response from the OpenWeather 5-Day Forecast API."""
    def __init__(self, data: dict | str, mode: Literal["json", "xml"]='json'):
        """
        Initializes the FiveDayForecastResponse with the provided data.

        Depending on the mode, the available data may vary as some fields are not present in XML or HTML responses, while other fields are not present in JSON format.

        :param data: A dictionary containing the response data from the 5-Day Forecast API.
        :param mode: The mode of the response, can be 'json', or 'xml', Defaults to 'json'.
        """
        self.data = data
        self.mode = mode

    def get_message(self) -> int:
        """
        Returns the message from the response data.
        The message is typically an integer representing the status of the response.

        The message is an internal parameter.

        Returns None if the mode is 'xml' since the message is not available in those formats.

        :return message: Message as an integer or None.
        """
        if self.mode == 'xml':
            return 0
        else:
            return self.data.get('message', 0)

    def get_count(self) -> int:
        """
        Returns the count of forecast entries from the response data.
        The count is typically an integer representing the number of forecast entries.

        The count is an internal parameter.

        Returns an empty list if the mode is 'xml' since the count is not available in those formats.

        :return count: Count of forecast entries as an integer.
        """
        if self.mode == 'xml':
            return 0
        else:
            return self.data.get('cnt', 0)

    def get_times(self) -> list[int]:
        """
        Returns the timestamps of the forecast data from the response data.
        The timestamps are typically represented as a Unix timestamp (seconds since epoch).

        Returns an empty list if the mode is 'xml' since the timestamp is not available in those formats.

        :return timestamp: Timestamp as an integer (Unix timestamp).
        """
        if self.mode == 'xml':
            return []
        else:
            return [entry.get('dt', 0) for entry in self.data.get('list', [])]

    def get_temperature(self) -> list[float]:
        """
        Returns a list of temperatures for each forecast entry.

        :return temperature: List of temperatures (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            temperatures = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                temperature = entry.find('temperature')
                if temperature is not None:
                    temperatures.append(float(temperature.get('value', 0.0)))
                else:
                    temperatures.append(0.0)
            return temperatures
        else:
            return [entry.get('main', {}).get('temp', 0.0) for entry in self.data.get('list', [])]

    def get_temperature_unit(self) -> list[str]:
        """
        Returns the units of the temperature from the response data.
        The units are typically 'Celsius' for metric or 'Fahrenheit' for imperial.

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return temperature_unit: Temperature unit as a string.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                temperature = entry.find('temperature')
                if temperature is not None:
                    units.append(temperature.get('unit', None))
                else:
                    units.append(None)
            return units
        else:
            return []

    def get_feels_like(self) -> list[float]:
        """
        Returns a list of feels-like temperatures for each forecast entry.
        Feels-like temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return feels_like: List of feels-like temperatures (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            feels_like_temps = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    feels_like = entry.find('feels_like')
                    if feels_like is not None:
                        feels_like_temps.append(float(feels_like.get('value', 0.0)))
                    else:
                        feels_like_temps.append(0.0)
            else:
                feels_like_temps = []
            return feels_like_temps
        else:
            return [entry.get('main', {}).get('feels_like', 0.0) for entry in self.data.get('list', [])]

    def get_feels_like_unit(self) -> list[str | None]:
        """
        Returns the units of the feels-like temperature from the response data.
        The units are typically 'Celsius' for metric or 'Fahrenheit' for imperial.

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return feels_like_unit: Feels-like temperature unit as a string.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    feels_like = entry.find('feels_like')
                    if feels_like is not None:
                        units.append(feels_like.get('unit', None))
                    else:
                        units.append(None)
            else:
                units = []
            return units
        else:
            return []

    def get_temperature_min(self) -> list[float]:
        """
        Returns a list of minimum temperatures for each forecast entry.
        Minimum temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return min_temperature: List of minimum temperatures (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            min_temps = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                temperature = entry.find('temperature')
                if temperature is not None:
                    min_temps.append(float(temperature.get('min', 0.0)))
                else:
                    min_temps.append(0.0)
            return min_temps
        else:
            return [entry.get('main', {}).get('temp_min', 0.0) for entry in self.data.get('list', [])]

    def get_temperature_max(self) -> list[float]:
        """
        Returns a list of maximum temperatures for each forecast entry.
        Maximum temperature is typically measured in degrees Celsius (°C) or Fahrenheit (°F).

        :return max_temperature: List of maximum temperatures (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            max_temps = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                temperature = entry.find('temperature')
                if temperature is not None:
                    max_temps.append(float(temperature.get('max', 0.0)))
                else:
                    max_temps.append(0.0)
            return max_temps
        else:
            return [entry.get('main', {}).get('temp_max', 0.0) for entry in self.data.get('list', [])]

    def get_pressure(self) -> list[int | None]:
        """
        Returns a list of atmospheric pressures for each forecast entry.
        Pressure is typically measured in hPa (hectopascals).

        :return pressure: List of atmospheric pressures (integers).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            pressures = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                pressure = entry.find('pressure')
                if pressure is not None:
                    pressures.append(int(pressure.get('value', 0)))
                else:
                    pressures.append(0)
            return pressures
        else:
            return [entry.get('main', {}).get('pressure', 0) for entry in self.data.get('list', [])]

    def get_pressure_unit(self) -> list[str | None]:
        """
        Returns the units of the atmospheric pressure from the response data.
        The units are typically 'hPa' (hectopascals).

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return pressure_unit: Atmospheric pressure unit as a string.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                pressure = entry.find('pressure')
                if pressure is not None:
                    units.append(pressure.get('unit', None))
                else:
                    units.append(None)
            return units
        else:
            return []

    def get_sea_level_pressure(self) -> list[int]:
        """
        Returns a list of sea level pressures for each forecast entry.
        Sea level pressure is typically measured in hPa (hectopascals).

        Returns an empty list if the mode is 'xml' since sea level pressure is not available in those formats.

        :return sea_level_pressure: List of sea level pressures (integers).
        """
        if self.mode == 'xml':
            return []
        else:
            return [entry.get('main', {}).get('sea_level', 0) for entry in self.data.get('list', [])]

    def get_ground_level_pressure(self) -> list[int]:
        """
        Returns a list of ground level pressures for each forecast entry.
        Ground level pressure is typically measured in hPa (hectopascals).

        Returns an empty list if the mode is 'xml' since ground level pressure is not available in those formats.

        :return ground_level_pressure: List of ground level pressures (integers).
        """
        if self.mode == 'xml':
            return []
        else:
            return [entry.get('main', {}).get('grnd_level', 0) for entry in self.data.get('list', [])]

    def get_humidity(self) -> list[int | None]:
        """
        Returns a list of humidity values for each forecast entry.
        Humidity is typically measured as a percentage (0-100%).

        :return humidity: List of humidity values (integers).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            humidities = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    humidity = entry.find('humidity')
                    if humidity is not None:
                        humidities.append(int(humidity.get('value', 0)))
                    else:
                        humidities.append(0)
            else:
                humidities = []
            return humidities
        else:
            return [entry.get('main', {}).get('humidity', 0) for entry in self.data.get('list', [])]

    def get_humidity_unit(self) -> list[str | None]:
        """
        Returns the units of the humidity from the response data.
        The units are typically 'percent' for percentage.

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return humidity_unit: Humidity unit as a string.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    humidity = entry.find('humidity')
                    if humidity is not None:
                        units.append(humidity.get('unit', None))
                    else:
                        units.append(None)
            else:
                units = []
            return units
        else:
            return []

    def get_weather_id(self) -> list[int]:
        """
        Returns a list of weather condition IDs for each forecast entry.
        Weather condition IDs are typically integers representing different weather conditions.

        :return weather_id: List of weather condition IDs (integers).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            weather_ids = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                symbol = entry.find('symbol')
                if symbol is not None:
                    weather_ids.append(int(symbol.get('number', -1)))
                else:
                    weather_ids.append(0)
            return weather_ids
        else:
            return [entry.get('weather', [{}])[0].get('id', -1) for entry in self.data.get('list', [])]

    def get_weather_main(self) -> list[str | None]:
        """
        Returns a list of main weather conditions for each forecast entry.
        Main weather conditions are typically strings representing the general weather condition (e.g., 'Clear', 'Clouds', 'Rain').

        Returns an empty list if the mode is 'xml' since main weather conditions are not available in those formats.

        :return weather_main: List of main weather conditions (strings).
        """
        if self.mode == 'xml':
            return []
        else:
            return [entry.get('weather', [{}])[0].get('main', None) for entry in self.data.get('list', [])]

    def get_weather_description(self) -> list[str | None]:
        """
        Returns a list of weather condition descriptions for each forecast entry.
        Weather condition descriptions are typically strings providing more detailed information about the weather (e.g., 'clear sky', 'few clouds').

        :return weather_description: List of weather condition descriptions (strings).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            weather_mains = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                symbol = entry.find('symbol')
                if symbol is not None:
                    weather_mains.append(symbol.get('name', None))
                else:
                    weather_mains.append(None)
            return weather_mains
        else:
            return [entry.get('weather', [{}])[0].get('description', None) for entry in self.data.get('list', [])]

    def get_weather_icon(self) -> list[str | None]:
        """
        Returns a list of weather condition icons for each forecast entry.
        Weather condition icons are typically strings representing the icon code for the weather condition.

        :return weather_icon: List of weather condition icons (strings).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            weather_icons = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                symbol = entry.find('symbol')
                if symbol is not None:
                    weather_icons.append(symbol.get('var', None))
                else:
                    weather_icons.append(None)
            return weather_icons
        else:
            return [entry.get('weather', [{}])[0].get('icon', None) for entry in self.data.get('list', [])]

    def get_clouds(self) -> list[int]:
        """
        Returns a list of cloudiness values for each forecast entry.
        Cloudiness is typically measured as a percentage (0-100%).

        :return clouds: List of cloudiness values (integers).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            clouds_list = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    clouds = entry.find('clouds')
                    if clouds is not None:
                        clouds_list.append(int(clouds.get('all', 0)))
                    else:
                        clouds_list.append(0)
            else:
                clouds_list = []
            return clouds_list
        else:
            return [entry.get('clouds', {}).get('all', 0) for entry in self.data.get('list', [])]

    def get_clouds_name(self) -> list[str | None]:
        """
        Returns a list of cloudiness names for each forecast entry.
        The cloudiness name is typically a string representing the cloudiness category (e.g., 'clear', 'cloudy').

        Returns an empty list if the mode is 'json' since the name is not available in that format.

        :return clouds_name: List of cloudiness names (strings).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            clouds_list = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    clouds = entry.find('clouds')
                    if clouds is not None:
                        clouds_list.append(clouds.get('value', None))
                    else:
                        clouds_list.append(None)
            else:
                clouds_list = []
            return clouds_list
        else:
            return []

    def get_clouds_unit(self) -> list[str | None]:
        """
        Returns the units of the cloudiness from the response data.
        The units are typically 'percent' for percentage.

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return clouds_unit: Cloudiness unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    clouds = entry.find('clouds')
                    if clouds is not None:
                        units.append(clouds.get('unit', None))
                    else:
                        units.append(None)
            else:
                units = []
            return units
        else:
            return []

    def get_wind_speed(self) -> list[float]:
        """
        Returns a list of wind speeds for each forecast entry.
        Wind speed is typically measured in meters per second (m/s).

        :return wind_speed: List of wind speeds (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind_speeds = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windSpeed')
                if wind is not None:
                    wind_speeds.append(float(wind.get('mps', 0.0)))
                else:
                    wind_speeds.append(0.0)
            return wind_speeds
        else:
            return [entry.get('wind', {}).get('speed', 0.0) for entry in self.data.get('list', [])]

    def get_wind_speed_unit(self) -> list[str | None]:
        """
        Returns the units of the wind speed from the response data.
        The units are typically 'm/s' (meters per second).

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return wind_speed_unit: Wind speed unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windSpeed')
                if wind is not None:
                    units.append(wind.get('unit', None))
                else:
                    units.append(None)
            return units
        else:
            return []

    def get_wind_speed_name(self) -> list[str | None]:
        """
        Returns a list of wind speed names for each forecast entry.
        The wind speed name is typically a string representing the wind speed category (e.g., 'calm', 'light breeze').

        Returns an empty list if the mode is 'json' since the name is not available in that format.

        :return wind_speed_name: List of wind speed names (strings).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind_speed_names = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windSpeed')
                if wind is not None:
                    wind_speed_names.append(wind.get('name', None))
                else:
                    wind_speed_names.append(None)
            return wind_speed_names
        else:
            return []

    def get_wind_deg(self) -> list[float]:
        """
        Returns a list of wind degrees for each forecast entry.
        Wind degrees are typically measured in degrees (0-360).

        :return wind_deg: List of wind degrees (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind_degrees = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windDirection')
                if wind is not None:
                    wind_degrees.append(float(wind.get('deg', 0.0)))
                else:
                    wind_degrees.append(0.0)
            return wind_degrees
        else:
            return [entry.get('wind', {}).get('deg', 0.0) for entry in self.data.get('list', [])]

    def get_wind_direction(self) -> list[str | None] | None:
        """
        Returns a list of wind directions for each forecast entry.
        Wind direction is typically represented as a string (e.g., 'N', 'NE', 'E', etc.).

        Returns an empty list if the mode is 'json' since wind direction is not available in those formats.

        :return wind_direction: List of wind directions (strings).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind_directions = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windDirection')
                if wind is not None:
                    wind_directions.append(wind.get('code', None))
                else:
                    wind_directions.append(None)
            return wind_directions
        else:
            return []

    def get_wind_direction_full(self) -> list[str | None]:
        """
        Returns a list of full wind directions for each forecast entry.
        Full wind direction is typically represented as a string (e.g., 'North', 'Northeast', 'East', etc.).

        Returns an empty list if the mode is 'json' since full wind direction is not available in those formats.

        :return wind_direction_full: List of full wind directions (strings).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind_direction_fulls = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windDirection')
                if wind is not None:
                    wind_direction_fulls.append(wind.get('name', None))
                else:
                    wind_direction_fulls.append(None)
            return wind_direction_fulls
        else:
            return []

    def get_wind_gust(self) -> list[float]:
        """
        Returns a list of wind gusts for each forecast entry.
        Wind gusts are typically measured in meters per second (m/s).

        :return wind_gust: List of wind gusts (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            wind_gusts = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windGust')
                if wind is not None:
                    wind_gusts.append(float(wind.get('gust', 0.0)))
                else:
                    wind_gusts.append(0.0)
            return wind_gusts
        else:
            return [entry.get('wind', {}).get('gust', 0.0) for entry in self.data.get('list', [])]

    def get_wind_gust_unit(self) -> list[str | None]:
        """
        Returns the units of the wind gust from the response data.
        The units are typically 'm/s' (meters per second).

        Returns an empty list if the mode is 'json' since the unit is not available in that format.

        :return wind_gust_unit: Wind gust unit as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            units = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                wind = entry.find('windGust')
                if wind is not None:
                    units.append(wind.get('unit', None))
                else:
                    units.append(None)
            return units
        else:
            return []

    def get_visibility(self) -> list[int]:
        """
        Returns a list of visibility values for each forecast entry.
        Visibility is typically measured in meters (m).

        :return visibility: List of visibility values (integers).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            visibilities = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                visibility = entry.find('visibility')
                if visibility is not None:
                    visibilities.append(int(visibility.get('value', 0)))
                else:
                    visibilities.append(0)
            return visibilities
        else:
            return [entry.get('visibility', 0) for entry in self.data.get('list', [])]

    def get_pop(self) -> list[float]:
        """
        Returns a list of probability of precipitation (POP) values for each forecast entry.
        The values of the parameter vary between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%

        :return pop: List of POP values (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            pops = []
            forecast = root.find('forecast')
            if forecast is not None:
                for entry in forecast.findall('time'):
                    pop = entry.find('precipitation')
                    if pop is not None:
                        pops.append(float(pop.get('probability', 0.0)))
                    else:
                        pops.append(0.0)
            else:
                pops = []
            return pops
        else:
            return [entry.get('pop', 0.0) for entry in self.data.get('list', [])]

    def get_rain(self) -> list[float]:
        """
        Returns a list of rain volume for each forecast entry.
        Rain volume is typically measured in millimeters (mm).

        :return rain: List of rain volumes (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            rains = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                precipitation = entry.find('precipitation')
                if precipitation is not None:
                    if precipitation.get('type') == 'rain':
                        rains.append(float(precipitation.get('value', 0.0)))
                    else:
                        rains.append(0.0)
                else:
                    rains.append(0.0)
            return rains
        else:
            return [entry.get('rain', {}).get('3h', 0.0) for entry in self.data.get('list', [])]

    def get_snow(self) -> list[float]:
        """
        Returns a list of snow volume for each forecast entry.
        Snow volume is typically measured in millimeters (mm).

        :return snow: List of snow volumes (floats).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            snows = []
            forecast = root.find('forecast')
            for entry in forecast.findall('time'):
                precipitation = entry.find('precipitation')
                if precipitation is not None:
                    if precipitation.get('type') == 'snow':
                        snows.append(float(precipitation.get('value', 0.0)))
                    else:
                        snows.append(0.0)
                else:
                    snows.append(0.0)
            return snows
        else:
            return [entry.get('snow', {}).get('3h', 0.0) for entry in self.data.get('list', [])]

    def get_part_of_day(self) -> list[str | None]:
        """
        Returns a list of part of day for each forecast entry.
        Part of day is typically represented as a string (n - night, d - day).

        Returns an empty list if the mode is 'xml' since part of day is not available in those formats.

        :return part_of_day: List of part of day (strings).
        """
        if self.mode == 'xml':
            return []
        else:
            return [entry.get('sys', {}).get('pod', None) for entry in self.data.get('list', [])]

    def get_city_id(self) -> int:
        """
        Returns the city ID from the response data.
        The city ID is typically an integer representing the unique identifier of the city.

        Returns -1 if the mode is 'xml' since city ID is not available in those formats.

        :return city_id: City ID as an integer or None.
        """
        if self.mode == 'xml':
            return -1
        else:
            return self.data.get('city', {}).get('id', -1)

    def get_city_name(self) -> str | None:
        """
        Returns the city name from the response data.
        The city name is typically a string representing the name of the city.

        :return city_name: City name as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                name = location.find('name')
                if name is not None:
                    return name.text
        else:
            return self.data.get('city', {}).get('name', None)

    def get_latitude(self) -> float | None:
        """
        Returns the latitude of the city from the response data.
        Latitude is typically a float representing the geographical coordinate.

        :return latitude: Latitude as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                location2 = location.find('location')
                if location2 is not None:
                    return float(location2.get('latitude', 0.0))
            return None
        else:
            return self.data.get('city', {}).get('coord', {}).get('lat', 0.0)

    def get_longitude(self) -> float | None:
        """
        Returns the longitude of the city from the response data.
        Longitude is typically a float representing the geographical coordinate.

        :return longitude: Longitude as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                location2 = location.find('location')
                if location2 is not None:
                    return float(location2.get('longitude', 0.0))
            return None
        else:
            return self.data.get('city', {}).get('coord', {}).get('lon', 0.0)

    def get_country(self) -> str | None:
        """
        Returns the country code from the response data.
        The country code is typically a string representing the ISO 3166-1 alpha-2 code of the country.

        :return country: Country code as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                country = location.find('country')
                if country is not None:
                    return country.text
            return None
        else:
            return self.data.get('city', {}).get('country', None)

    def get_population(self) -> int:
        """
        Returns the population of the city from the response data.
        The population is typically an integer representing the number of inhabitants in the city.

        Returns -1 if the mode is 'xml' since population is not available in those formats.

        :return population: Population as an integer.
        """
        if self.mode == 'xml':
            return -1
        else:
            return self.data.get('city', {}).get('population', -1)

    def get_timezone(self) -> int:
        """
        Returns the timezone offset from the response data.
        The timezone offset is typically an integer representing the offset in seconds from UTC.

        :return timezone: Timezone offset as an integer.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                return int(location.find('timezone').text)
            return -1
        else:
            return self.data.get('city', {}).get('timezone', -1)

    def get_sunrise(self) -> str | int:
        """
        Returns the sunrise time from the response data.
        The sunrise time is typically represented as a Unix timestamp (seconds since epoch).

        :return sunrise: Sunrise time as an integer (Unix timestamp) or in the `ISO 8601`_ format.

        .. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            sun = root.find('sun')
            if sun is not None:
                return sun.get('rise', "1970-01-01T00:00:00Z")
            return -1
        else:
            return self.data.get('city', {}).get('sunrise', -1)

    def get_sunset(self) -> str | int:
        """
        Returns the sunset time from the response data.
        The sunset time is typically represented as a Unix timestamp (seconds since epoch).

        :return sunset: Sunset time as an integer (Unix timestamp) or in the `ISO 8601`_ format.

        .. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            sun = root.find('sun')
            if sun is not None:
                return sun.get('set', "1970-01-01T00:00:00Z")
            return -1
        else:
            return self.data.get('city', {}).get('sunset', -1)

    def get_altitude(self) -> float:
        """
        Returns the altitude of the city from the response data.
        The altitude is typically a float representing the height above sea level in meters.

        Returns -1.0 if the mode is 'json' since altitude is not available in those formats.

        :return altitude: Altitude as a float or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                location2 = location.find('location')
                if location2 is not None:
                    return float(location2.get('altitude', -1.0))
            return -1.0
        else:
            return -1.0

    def get_geobase(self) -> str | None:
        """
        Returns the geobase of the city from the response data.
        The geobase is typically a string representing the geographical base of the city.

        Returns an empty string if the mode is 'json' since geobase is not available in those formats.

        :return geobase: Geobase as a string or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                location2 = location.find('location')
                if location2 is not None:
                    return location2.get('geobase', None)
            return None
        else:
            return None

    def get_geobase_id(self) -> int:
        """
        Returns the geobase ID of the city from the response data.
        The geobase ID is typically an integer representing the unique identifier of the geographical base.

        Returns -1 if the mode is 'json' since geobase ID is not available in those formats.

        :return geobase_id: Geobase ID as an integer or None.
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            location = root.find('location')
            if location is not None:
                location2 = location.find('location')
                if location2 is not None:
                    return int(location2.get('geobaseid', -1))
            return -1
        else:
            return -1

    def get_lastupdate(self) -> int | None:
        """
        Returns the last update time from the response data.
        The last update time is typically represented as a Unix timestamp (seconds since epoch).

        Returns -1 if the mode is 'json' since last update time is not available in those formats.

        :return last_update: Last update time as an integer (Unix timestamp).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            meta = root.find('meta')
            if meta is not None:
                return meta.find('lastupdate').text
            return -1
        else:
            return -1

    def get_calctime(self) -> int:
        """
        Returns the calculation time from the response data.
        The calculation time is typically represented as a Unix timestamp (seconds since epoch).

        Returns -1 if the mode is 'json' since calculation time is not available in those formats.

        :return calc_time: Calculation time as an integer (Unix timestamp).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            meta = root.find('meta')
            if meta is not None:
                calctime = meta.find('calctime')
                if calctime is not None:
                    return calctime.text
            return -1
        else:
            return -1

    def get_next_update(self) -> int:
        """
        Returns the next update time from the response data.
        The next update time is typically represented as a Unix timestamp (seconds since epoch).

        Returns -1 if the mode is 'json' since next update time is not available in those formats.

        :return next_update: Next update time as an integer (Unix timestamp).
        """
        if self.mode == 'xml':
            root = ET.fromstring(self.data)
            meta = root.find('meta')
            if meta is not None:
                return meta.find('nextupdate').text
            return -1
        else:
            return -1

class AirPollutionResponse:
    """
    Class to handle the response data for air pollution information.
    It provides methods to extract various air quality parameters from the response data.
    """

    def __init__(self, data: dict):
        """
        Initializes the AirPollutionResponse with the provided data and mode.

        :param data: The response data as a dictionary or XML string.
        :param mode: The format of the response data ('json' or 'xml').
        """
        self.data = data

    def get_coord(self) -> list[int]:
        """
        Returns the coordinates of the location from the response data.
        The coordinates are typically represented as a list of two integers [longitude, latitude].

        :return coord: List of coordinates [longitude, latitude].
        """
        return self.data.get('coord', [0, 0])

    def get_times(self) -> list[int]:
        """
        Returns a list of timestamps for the air pollution data.
        The timestamps are typically represented as Unix timestamps (seconds since epoch).

        :return times: List of timestamps (integers).
        """
        return [entry.get('dt', 0) for entry in self.data.get('list', [])]

    def get_aqi(self) -> list[int]:
        """
        Returns a list of Air Quality Index (AQI) values for the air pollution data.
        The AQI is typically an integer representing the air quality level.

        :return aqi: List of AQI values (integers).
        """
        return [entry.get('main', {}).get('aqi', 0) for entry in self.data.get('list', [])]

    def get_carbon_monoxide(self) -> list[float]:
        """
        Returns a list of carbon monoxide (CO) levels for the air pollution data.
        The CO levels are typically measured in micrograms per cubic meter (µg/m³).

        :return carbon_monoxide: List of CO levels (floats).
        """
        return [entry.get('components', {}).get('co', 0.0) for entry in self.data.get('list', [])]

    def get_nitrogen_monoxide(self) -> list[float]:
        """
        Returns a list of nitrogen monoxide (NO) levels for the air pollution data.
        The NO levels are typically measured in micrograms per cubic meter (µg/m³).

        :return nitrogen_monoxide: List of NO levels (floats).
        """
        return [entry.get('components', {}).get('no', 0.0) for entry in self.data.get('list', [])]

    def get_nitrogen_dioxide(self) -> list[float]:
        """
        Returns a list of nitrogen dioxide (NO₂) levels for the air pollution data.
        The NO₂ levels are typically measured in micrograms per cubic meter (µg/m³).

        :return nitrogen_dioxide: List of NO₂ levels (floats).
        """
        return [entry.get('components', {}).get('no2', 0.0) for entry in self.data.get('list', [])]

    def get_ozone(self) -> list[float]:
        """
        Returns a list of ozone (O₃) levels for the air pollution data.
        The O₃ levels are typically measured in micrograms per cubic meter (µg/m³).

        :return ozone: List of O₃ levels (floats).
        """
        return [entry.get('components', {}).get('o3', 0.0) for entry in self.data.get('list', [])]

    def get_sulphur_dioxide(self) -> list[float]:
        """
        Returns a list of sulphur dioxide (SO₂) levels for the air pollution data.
        The SO₂ levels are typically measured in micrograms per cubic meter (µg/m³).

        :return sulphur_dioxide: List of SO₂ levels (floats).
        """
        return [entry.get('components', {}).get('so2', 0.0) for entry in self.data.get('list', [])]

    def get_pm2_5(self) -> list[float]:
        """
        Returns a list of PM2.5 (particulate matter with a diameter of less than 2.5 micrometers) levels for the air pollution data.
        The PM2.5 levels are typically measured in micrograms per cubic meter (µg/m³).

        :return pm2_5: List of PM2.5 levels (floats).
        """
        return [entry.get('components', {}).get('pm2_5', 0.0) for entry in self.data.get('list', [])]

    def get_pm10(self) -> list[float]:
        """
        Returns a list of PM10 (particulate matter with a diameter of less than 10 micrometers) levels for the air pollution data.
        The PM10 levels are typically measured in micrograms per cubic meter (µg/m³).

        :return pm10: List of PM10 levels (floats).
        """
        return [entry.get('components', {}).get('pm10', 0.0) for entry in self.data.get('list', [])]

    def get_ammonia(self) -> list[float]:
        """
        Returns a list of ammonia (NH₃) levels for the air pollution data.
        The NH₃ levels are typically measured in micrograms per cubic meter (µg/m³).

        :return ammonia: List of NH₃ levels (floats).
        """
        return [entry.get('components', {}).get('nh3', 0.0) for entry in self.data.get('list', [])]

class GeocodingResponse:
    """
    Class to handle the response data for geocoding information.
    It provides methods to extract various geocoding parameters from the response data.
    """

    def __init__(self, data: dict | list[dict]) -> None:
        """
        Initializes the GeocodingResponse with the provided data.

        :param data: The response data as a dictionary.
        """
        self.data = data

    def get_name(self) -> list[str | None] | str | None:
        """
        Returns the name of the location from the response data.
        The name is typically a string representing the name of the location.

        :return name: Location name as a string or None.
        """
        if isinstance(self.data, list):
            return [entry.get('name', None) for entry in self.data]
        else:
            return self.data.get('name', None)

    def get_local_names(self) -> list[dict[str, str]] | dict[str, str]:
        """
        Returns a dictionary of local names for the location from the response data.
        Local names are typically represented as a dictionary with language codes as keys and names as values.

        :return local_names: Dictionary of local names (language code: name).
        """
        if isinstance(self.data, list):
            return [entry.get('local_names', {}) for entry in self.data]
        else:
            return self.data.get('local_names', {})

    def get_latitude(self) -> list[float] | float:
        """
        Returns the latitude of the location from the response data.
        Latitude is typically a float representing the geographical coordinate.

        :return latitude: Latitude as a float.
        """
        if isinstance(self.data, list):
            return [entry.get('lat', 0.0) for entry in self.data]
        else:
            return self.data.get('lat', 0.0)

    def get_longitude(self) -> list[float] | float:
        """
        Returns the longitude of the location from the response data.
        Longitude is typically a float representing the geographical coordinate.

        :return longitude: Longitude as a float.
        """
        if isinstance(self.data, list):
            return [entry.get('lon', 0.0) for entry in self.data]
        else:
            return self.data.get('lon', 0.0)

    def get_country(self) -> list[str | None] | str | None:
        """
        Returns the country code from the response data.
        The country code is typically a string representing the ISO 3166-1 alpha-2 code of the country.

        :return country: Country code as a string or None.
        """
        if isinstance(self.data, list):
            return [entry.get('country', None) for entry in self.data]
        else:
            return self.data.get('country', None)

    def get_state(self) -> list[str | None] | str | None:
        """
        Returns the state or region from the response data.
        The state is typically a string representing the name of the state or region.

        :return state: State or region as a string or None.
        """
        if isinstance(self.data, list):
            return [entry.get('state', None) for entry in self.data]
        else:
            return self.data.get('state', None)

    def get_zip(self) -> str | None:
        """
        Returns the zip code specified in the API request.

        :return zip: Zip code as a string or None.
        """
        if isinstance(self.data, list):
            return None
        return self.data.get('zip', None)
