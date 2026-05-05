from pydantic import BaseModel

class PairingCodeRequest(BaseModel):
    desktop_device_id: str


class PairingCodeResponse(BaseModel):
    pairing_code: str
    qr_payload: str

