from pydantic import BaseModel


class DeviceLinkRequest(BaseModel):
    desktop_device_id: str
