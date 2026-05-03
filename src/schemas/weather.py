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

class currentWeatherResponse(BaseModel):
    weather_main: str
    description: str
    icon: str
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int

'''
aqi: 공기질 지수 aqi (1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor)
aqi_label: "좋음" "보통" "나쁨"
pm2_5: 초미세먼지
pm10: 미세먼지
status: UI 상태값
'''

class AirPollutionResponse(BaseModel):
    aqi: int
    aqi_label: str
    pm2_5: float
    pm10: float
    status: str
