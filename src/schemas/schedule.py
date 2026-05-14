from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ScheduleCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: Optional[datetime] = None


class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
