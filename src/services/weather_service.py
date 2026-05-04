import os

from dotenv import load_dotenv
import httpx

from src.schemas.weather import WeatherForecastResponse
from src.schemas.weather import currentWeatherResponse
from src.schemas.weather import airPollutionResponse

load_dotenv()

def get_forecast_weather(city: str) -> WeatherForecastResponse:
    url = os.getenv("OPENWEATHER_FORECAST_API_URL") 

    if not url:
        raise RuntimeError("OPENWEATHER_FORECAST_API_URL is required")
    

    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)

    response.raise_for_status()
    data = response.json()

    items = []

    for item in data["list"]:
        weather = item["weather"][0]

        items.append(
            {
                "forecast_at": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "temp_min": item["main"]["temp_min"],
                "temp_max": item["main"]["temp_max"],
                "wind_speed": item["wind"]["speed"],
                "description": weather["description"],
                "icon": weather["icon"],
            }
        )
    
    return WeatherForecastResponse(
        items=items,
    )


def get_current_weather(city: str) -> currentWeatherResponse:
    url = os.getenv("OPENWEATHER_CURRENT_API_URL")

    if not url:
        raise RuntimeError("OPENWEATHER_CURRENT_API_URL is required")
    
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)

    response.raise_for_status()
    data = response.json()

    return (
        {
            "weather_main": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "temp_min": round(data["main"]["temp_min"]),
            "temp_max": round(data["main"]["temp_max"]),
            "humidity": data["main"]["humidity"],
        }
    );

def get_air_pollution(city: str) -> airPollutionResponse:
    url = os.getenv("OPENWEATHER_CURRENT_API_URL")

    if not url:
        raise RuntimeError("OPENWEATHER_CURRENT_API_URL is required")
    
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
