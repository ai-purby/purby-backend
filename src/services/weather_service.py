import os

from dotenv import load_dotenv
import httpx

from src.schemas.weather import WeatherForecastResponse

load_dotenv()

def get_forecast() -> WeatherForecastResponse:
    url = os.getenv("OPENWEATHER_API_URL")

    if not url:
        raise RuntimeError("OPENWEATHER_API_URL is required")
    

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


