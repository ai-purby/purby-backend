from fastapi import APIRouter, Query
from src.services.device_service import issue_pairing_code

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.post("/pairing-code")
async def create_pairing_code():
    return issue_pairing_code();
    
