from fastapi import APIRouter, Query
from src.services.weather_service import get_forecast

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

@router.get("")
def get_weather():
    return get_forecast()