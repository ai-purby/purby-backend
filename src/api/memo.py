from fastapi import APIRouter

from src.services.memo_service import create_memo_service
from src.schemas.memo import CreateMemoRequest, MemoResponse

router = APIRouter(
    prefix="/memos",
    tags=["memos"],
)

@router.post("", response_model=MemoResponse)
async def create_memo(body: CreateMemoRequest):
    return await create_memo_service(body)
