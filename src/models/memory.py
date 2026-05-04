# memories / memory_types / memory_categories / memory_embeddings
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Any
from sqlalchemy import String, DateTime, text, ForeignKey, Enum, Text, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.voice import ConversationEvent

# memories(id, user_id, conversation_event_id, memory_type_id, memory_category_id, value_text, value_json, summary, confidence, pinned, last_used_at, expires_at, created_at, updated_at)
class Memory(Base):
    # 테이블 이름
    __tablename__ = "memories"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        nullable = False
    )

    conversation_event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversation_events.id", ondelete = "CASCADE"),
        nullable = False
    )

    memory_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memory_types.id", ondelete = "CASCADE"),
        nullable = False
    )

    memory_category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memory_categories.id", ondelete = "CASCADE"),
        nullable = False
    )

    value_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    value_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True
    )

    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    confidence: Mapped[Optional[float]] = mapped_column(
        Numeric(4, 3),
        nullable= True
    )

    pinned: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
        nullable= False
    )

    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )  

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )  

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),  
        onupdate = text("now()"), 
        nullable = False
    )

    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "memories"
    )

    conversation_event: Mapped["ConversationEvent"] = relationship(
        "ConversationEvent", 
        back_populates = "memories"
    )

    type: Mapped["MemoryType"] = relationship(
        "MemoryType", 
        back_populates = "memories"
    )

    category: Mapped["MemoryCategory"] = relationship(
        "MemoryCategory", 
        back_populates = "memories"
    )

    embeddings: Mapped[list["MemoryEmbedding"]] = relationship(
        "MemoryEmbedding",
        back_populates= "memory",
        cascade= "all, delete-orphan"
    )

# memory_types(id, type)
class MemoryType(Base):
    # 테이블 이름
    __tablename__ = "memory_types"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    # 관계 지정
    memories: Mapped[list["Memory"]] = relationship(
        "Memory",
        back_populates= "type",
        cascade= "all, delete-orphan"
    )

# memory_categories(id, category)
class MemoryCategory(Base):
    # 테이블 이름
    __tablename__ = "memory_categories"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    # 관계 지정
    memories: Mapped[list["Memory"]] = relationship(
        "Memory",
        back_populates= "category",
        cascade= "all, delete-orphan"
    )

# memory_embeddings(id, memory_id, embedding_model, embedding_vector, chunk_text, created_at)
class MemoryEmbedding(Base):
    # 테이블 이름
    __tablename__ = "memory_embeddings"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    memory_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memories.id", ondelete = "CASCADE"),
        nullable = False
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    embedding_vector: Mapped[list[float]] = mapped_column(
        Vector(1536),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )  

    # 관계 지정
    memory: Mapped["Memory"] = relationship(
        "Memory", 
        back_populates = "embeddings"
    )