from fastapi import APIRouter
from src.schemas.device import PairingCodeResponse
from src.schemas.device import PairingCodeRequest

from src.services.device_service import issue_pairing_code

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.post("/pairing-code")
async def create_pairing_code(request: PairingCodeRequest) -> PairingCodeResponse:
    return await issue_pairing_code(request.desktop_device_id)
    
