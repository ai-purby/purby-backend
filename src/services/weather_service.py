import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
import httpx

from src.schemas.weather import WeatherForecastResponse
from src.schemas.weather import WeatherForecastItem
from src.schemas.weather import currentWeatherResponse
from src.schemas.weather import airPollutionResponse
from src.schemas.weather import WeatherResponse

load_dotenv()

def get_weather() -> WeatherResponse:
    current = get_current_weather()
    forecast = get_forecast_weather()
    air_pollution = get_air_pollution()
    current = apply_today_forecast_summary(current, forecast.items)

    return WeatherResponse(
        current=current,
        forecast=forecast.items,
        air_pollution=air_pollution,
    )


def get_forecast_weather() -> WeatherForecastResponse:
    url = os.getenv("OPENWEATHER_FORECAST_API_URL") 

    if not url:
        raise RuntimeError("OPENWEATHER_FORECAST_API_URL is required")
    

    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)

    response.raise_for_status()
    data = response.json()

    items = []
    now = datetime.now(ZoneInfo("Asia/Seoul")).replace(tzinfo=None)

    for item in data["list"]:
        forecast_at = datetime.fromisoformat(item["dt_txt"])
        if forecast_at < now:
            continue

        weather = item["weather"][0]

        items.append(
            {
                "forecast_at": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "temp_min": item["main"]["temp_min"],
                "temp_max": item["main"]["temp_max"],
                "wind_speed": item["wind"]["speed"],
                "pop": round(item.get("pop", 0) * 100),
                "description": weather["description"],
                "icon": weather["icon"],
            }
        )
    
    return WeatherForecastResponse(
        items=items,
    )


def get_current_weather() -> currentWeatherResponse:
    url = os.getenv("OPENWEATHER_CURRENT_API_URL")

    if not url:
        raise RuntimeError("OPENWEATHER_CURRENT_API_URL is required")
    
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)

    response.raise_for_status()
    data = response.json()

    return currentWeatherResponse(
        weather_main=data["weather"][0]["main"],
        description=data["weather"][0]["description"],
        icon=data["weather"][0]["icon"],
        temp=round(data["main"]["temp"]),
        feels_like=round(data["main"]["feels_like"]),
        temp_min=round(data["main"]["temp_min"]),
        temp_max=round(data["main"]["temp_max"]),
        humidity=data["main"]["humidity"],
        pop=0,
    )

def get_air_pollution() -> airPollutionResponse:
    url = os.getenv("OPENWEATHER_AIR_POLLUTION_API_URL")

    if not url:
        raise RuntimeError("OPENWEATHER_AIR_POLLUTION_API_URL is required")
    
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)

    response.raise_for_status()
    data = response.json()

    pollution = data["list"][0]
    aqi = pollution["main"]["aqi"]
    components = pollution["components"]

    labels = {
        1: ("좋음", "good"),
        2: ("좋음", "good"),
        3: ("보통", "normal"),
        4: ("나쁨", "bad"),
        5: ("나쁨", "bad"),
    }
    aqi_label, status = labels.get(aqi, ("알 수 없음", "unknown"))

    return airPollutionResponse(
        aqi=aqi,
        aqi_label=aqi_label,
        pm2_5=components["pm2_5"],
        pm10=components["pm10"],
        status=status,
    )

def apply_today_forecast_summary(
    current: currentWeatherResponse,
    items: list[WeatherForecastItem],
) -> currentWeatherResponse:
    today_date = datetime.now(ZoneInfo("Asia/Seoul")).date()

    today_items = [
        item for item in items
        if datetime.fromisoformat(item.forecast_at).date() == today_date
    ]

    if not today_items:
        return current

    return current.model_copy(update={
        "temp_min": round(min(item.temp_min for item in today_items)),
        "temp_max": round(max(item.temp_max for item in today_items)),
        "pop": max(item.pop for item in today_items),
    })
