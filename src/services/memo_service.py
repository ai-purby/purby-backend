from src.core.database import AsyncSessionLocal
from src.models import briefing, character, device, memory, schedule, system, user, voice  # noqa: F401
from src.models.memo import Memo
from src.schemas.memo import CreateMemoRequest


async def create_memo_service(body: CreateMemoRequest) -> Memo:
    memo = Memo(
        user_id=body.user_id,
        content=body.content,
        is_pinned=body.is_pinned,
    )

    async with AsyncSessionLocal() as session:
        session.add(memo)
        await session.commit()
        await session.refresh(memo)

    return memo
