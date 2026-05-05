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
async def get_weather():
        return await get_weather()

