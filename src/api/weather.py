from fastapi import APIRouter, Query
from src.services.weather_service import get_current_weather
from src.services.weather_service import get_forecast_weather
from src.services.weather_service import get_air_pollution
from enum import Enum

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

class WeatherType(str, Enum):
    current = "current"
    forecast = "forecast"
    air_pollution = "air_pollution"

@router.get("")
async def get_weather(type: WeatherType, city: str):
    if type == WeatherType.current:
        return await get_current_weather(city)

    if type == WeatherType.forecast:
        return await get_forecast_weather(city)

    if type == WeatherType.air_pollution:
        return await get_air_pollution(city)

