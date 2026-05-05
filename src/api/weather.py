from fastapi import APIRouter

from src.schemas.weather import WeatherResponse
from src.services.weather_service import get_weather as get_weather_service

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

@router.get("")
async def get_weather():
    return get_weather_service()
