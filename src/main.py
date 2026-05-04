from fastapi import FastAPI
from src.api.weather import router as weather_router
from src.api.devices import router as devices_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(weather_router, prefix="/api")
app.include_router(devices_router, prefix="/api")
