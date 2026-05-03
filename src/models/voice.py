# voice_sessions / voice_commands / conversation_events
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Any
from sqlalchemy import DateTime, text, ForeignKey, Enum, Text, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.device import Device

# Enum Class
class VoiceStatus(str, enum.Enum):
    TIMEOUT = "timeout"
    FAIL = "fail"
    SUCCESS = "success"

class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    EXTRACTED = "extracted"
    FAILED = "failed"

# voice_sessions(id, user_id, device_id, wakeword_detected_at, started_at, ended_at, status, created_at)
class VoiceSession(Base):
    # 테이블 이름
    __tablename__ = "voice_sessions"

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

    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("devices.id", ondelete = "CASCADE"),
        nullable = False
    )

    wakeword_detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    status: Mapped[VoiceStatus] = mapped_column(
        Enum(VoiceStatus),
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )    
    
    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "voice_sessions"
    )

    device: Mapped["Device"] = relationship(
        "Device", 
        back_populates = "voice_sessions"
    )

    voice_commands: Mapped[list["VoiceCommand"]] = relationship(
        "VoiceCommand",
        back_populates= "voice_session",
        cascade= "all, delete-orphan"
    )

    conversation_events: Mapped[list["ConversationEvent"]] = relationship(
        "ConversationEvent",
        back_populates= "voice_session",
        cascade= "all, delete-orphan"
    )

# voice_commnands(id, voice_session_id, intent_code, raw_text, normalized_text, entities_json, requires_confirmation, result_summary, created_at)
class VoiceCommand(Base):
    # 테이블 이름
    __tablename__ = "voice_commands"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    voice_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("voice_sessions.id", ondelete = "CASCADE"),
        nullable = False
    )

    intent_code: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    normalized_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable = True
    )
    
    entities_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True
    )

    requires_confirmation: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
        nullable= False
    )

    result_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable= True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    # 관계 지정
    voice_session: Mapped["VoiceSession"] = relationship(
        "VoiceSession", 
        back_populates = "voice_commands"
    )


# converstaion_events(id, voice_session_id, user_id, raw_text, normalized_text, processing_status, occurred_at, created_at)
class ConversationEvent(Base): 
    # 테이블 이름
    __tablename__ = "conversation_events"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    voice_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("voice_sessions.id", ondelete = "CASCADE"),
        nullable = False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        nullable = False
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False   
    )

    normalized_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus),
        nullable = False
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    # 관계 지정
    voice_session: Mapped["VoiceSession"] = relationship(
        "VoiceSession", 
        back_populates = "conversation_events"
    )

    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "conversation_events"
    )

