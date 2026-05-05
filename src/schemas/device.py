from pydantic import BaseModel

class PairingCodeResponse(BaseModel):
    pairing_code: str
    expires_in: int
