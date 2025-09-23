"""
Calls OpenWeather API.
Service for fetching real-time weather data for Tokyo.
"""

from app.core.config import settings
from app.core.logger import logger
import requests

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self, city: str):
        url = f"{self.base_url}?q={city}&appid={self.api_key}"
        response = requests.get(url)
        return response.json()    

if __name__ == "__main__":
    weather_service = WeatherService()
    print(weather_service.get_weather("Tokyo"))