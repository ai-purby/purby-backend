from fastapi import APIRouter, Query
from src.services.weather_service import fetch_forecast
from src.services.weather_service import fetch_current

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

@router.get("/forecast")
def get_forecast():
    return fetch_forecast()

@router.get("/current")
def get_current():
    return fetch_current()

# @router.get("/pollution")
    return fetch_pollution()