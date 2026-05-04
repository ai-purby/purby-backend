from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.get("")
def hi():
    return "good"

