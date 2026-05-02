from fastapi import FastAPI
from src.api.weather import router as weather_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_method=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(weather_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}