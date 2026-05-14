from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, schedules, settings, devices, users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(schedules.router)
app.include_router(settings.router)
app.include_router(devices.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
