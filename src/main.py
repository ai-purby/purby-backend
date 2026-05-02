from fastapi import FastAPI
from src.api.weather import router as weather_router

app = FastAPI()

app.include_router(weather_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}