from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateMemoRequest(BaseModel):
    user_id: UUID
    content: str
    is_pinned: bool = False

class MemoResponse(BaseModel):
    id: UUID
    user_id: UUID
    content: str
    is_pinned: bool
    created_at: datetime
    updated_at: datetime
