"""Weather API integration utilities."""

import requests
from datetime import datetime


class WeatherAPI:
    """Fetch weather data from free weather API."""

    # Using Open-Meteo API (free, no API key required)
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    @staticmethod
    def get_weather_by_coordinates(latitude, longitude):
        """
        Get current weather data by latitude and longitude.
        Using Open-Meteo free weather API.
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,is_day",
                "timezone": "auto",
            }
            response = requests.get(WeatherAPI.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            weather_code = current.get("weather_code", 0)
            weather_description = WeatherAPI.get_weather_description(weather_code)

            weather_info = {
                "temperature": current.get("temperature_2m", "N/A"),
                "humidity": current.get("relative_humidity_2m", "N/A"),
                "weather": weather_description,
                "wind_speed": current.get("wind_speed_10m", "N/A"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            return weather_info
        except requests.RequestException as e:
            print(f"Error fetching weather: {e}")
            return None

    @staticmethod
    def get_location_coordinates(location_name):
        """Get coordinates for a location."""
        try:
            params = {"name": location_name, "count": 1, "language": "en", "format": "json"}
            response = requests.get(WeatherAPI.GEOCODE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                result = data["results"][0]
                return {
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "name": result.get("name"),
                    "country": result.get("country"),
                }
            return None
        except requests.RequestException as e:
            print(f"Error geocoding location: {e}")
            return None

    @staticmethod
    def get_weather_description(weather_code):
        """Convert WMO weather code to description."""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy (depositing rime)",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return weather_codes.get(weather_code, "Unknown")

    @staticmethod
    def get_default_weather():
        """Get default weather data (mock for demo)."""
        return {
            "temperature": 25.5,
            "humidity": 65,
            "weather": "Partly cloudy",
            "wind_speed": 12.5,
            "location": "Current Location",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


class SunriseSunset:
    """Fetch sunrise and sunset times."""

    BASE_URL = "https://api.sunrise-sunset.org/json"

    @staticmethod
    def get_sun_times(latitude, longitude):
        """Get sunrise and sunset times."""
        try:
            params = {"lat": latitude, "lng": longitude, "formatted": 0}
            response = requests.get(SunriseSunset.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK":
                results = data.get("results", {})
                return {
                    "sunrise": results.get("sunrise", "N/A"),
                    "sunset": results.get("sunset", "N/A"),
                }
            return None
        except requests.RequestException as e:
            print(f"Error fetching sun times: {e}")
            return None

    @staticmethod
    def get_default_sun_times():
        """Get default sun times (mock for demo)."""
        return {
            "sunrise": "06:00:00",
            "sunset": "18:30:00",
        }
