from pydantic import BaseModel
from typing import Optional


class SettingsUpdate(BaseModel):
    ai_name:          Optional[str]   = None
    personality:      Optional[str]   = None
    sleep_enabled:    Optional[bool]  = None
    sleep_start:      Optional[str]   = None
    sleep_end:        Optional[str]   = None
    briefing_enabled: Optional[bool]  = None
    briefing_time:    Optional[str]   = None
    retro_enabled:    Optional[bool]  = None
    retro_time:       Optional[str]   = None
    volume:           Optional[float] = None
    brightness:       Optional[float] = None
