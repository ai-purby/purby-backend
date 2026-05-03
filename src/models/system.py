# notifications / system_logs
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Any
from sqlalchemy import String, DateTime, text, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.device import Device

# Enum Class
class NotificationSourceType(str, enum.Enum) :
    SCHEDULE = "schedule"
    BRIEFING = "briefing"
    SYSTEM = "system"

class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"
    FAILED = "failed"

class SystemSource(str, enum.Enum):
    VOICE = "voice"
    DEVICE = "device"
    NOTIFICATION = "notification"

class SystemLevel(str, enum.Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


# notifications(id, user_id, source_type, source_id, title, body, scheduled_at, status, created_at)
class Notification(Base):
    # 테이블 이름
    __tablename__ = "notifications"

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

    source_type: Mapped[NotificationSourceType] = mapped_column(
        Enum(NotificationSourceType),
        nullable=False
    )

    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid = True),
        nullable=True
    )

    title: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    body: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    scheduled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )
        
    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "notifications"
    )
         

# system_logs(id, device_id, user_id, source, level, error_code, message, payload, occurred_at)
class SystemLog(Base):
    # 테이블 이름
    __tablename__ = "system_logs"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )    

    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("devices.id", ondelete = "CASCADE"),
        nullable = False
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        nullable = False
    )

    source: Mapped[SystemSource | None] = mapped_column(
        Enum(SystemSource),
        nullable= True
    )

    level: Mapped[SystemLevel] = mapped_column(
        Enum(SystemLevel),
        nullable=False
    )

    error_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    payload: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "system_logs"
    )

    device: Mapped["Device"] = relationship(
        "Device", 
        back_populates = "system_logs"
    )

    