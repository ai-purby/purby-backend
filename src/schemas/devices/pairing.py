from pydantic import BaseModel

class PairingStatusResponse(BaseModel):
    pairingCode: str
    status: str
    deviceToken: str | None = None
