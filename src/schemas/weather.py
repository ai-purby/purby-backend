from pydantic import BaseModel

class WeatherForecastItem(BaseModel):
    forecast_at: str
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    wind_speed: float
    description: str
    icon: str

class WeatherForecastResponse(BaseModel):
    items: list[WeatherForecastItem]