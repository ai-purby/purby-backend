# users / user_settings / auth_session
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime, time
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, text, ForeignKey, Time, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from src.models.device import Device
    from src.models.system import Notification
    from src.models.system import SystemLog


# Enum Class
class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"

# users(id, name, email, timezone, created_at, updated_at)
class User(Base):
    # 테이블 이름
    __tablename__ = "users"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    name: Mapped[str] = mapped_column(
        String(15),
        nullable = False
    )

    email: Mapped[str] = mapped_column(
        String(30),
        unique = True,
        nullable = False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    timezone: Mapped[str] = mapped_column(
        String(30),
        default = "Asia/Seoul",
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),  # 데이터가 처음 생성될 때 시간
        onupdate = text("now()"),  # 데이터가 수정될 때의 시간
        nullable = False
    )

    # 관계 지정
    settings: Mapped["UserSetting"] = relationship(
        "UserSetting", 
        back_populates = "user", 
        cascade = "all, delete-orphan"
    )

    sessions: Mapped[list["AuthSession"]] = relationship(
        "AuthSession",
        back_populates = "user",
        cascade= "all, delete-orphan"
    )

    devices: Mapped[list["Device"]] = relationship(
        "Device",
        back_populates = "user",
        cascade= "all, delete-orphan"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates= "user",
        cascade= "all, delete-orphan"
    )

    system_logs: Mapped[list["SystemLog"]] = relationship(
        "SystemLog",
        back_populates= "user",
        cascade= "all, delete-orphan"
    )

# user_settings(user_id, personality_id, remind_before_minutes, sleep_start_time, sleep_end_time, morning_briefing_time, evening_briefing_time, created_at, updated_at)
class UserSetting(Base):
    __tablename__ = "user_settings"

    # 식별자
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        primary_key = True
    )

    personality_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("character_personalities.id", ondelete = "SET DEFAULT"),
        server_default=text("'00000000-0000-0000-0000-000000000000'"),
        nullable = False  # 설정에서 캐릭터 성격 지정 안 하면 default 성격으로 들어감
    )
    
    remind_before_minutes: Mapped[Optional[int]] = mapped_column( 
        Integer,
        nullable = True
    )

    sleep_start_time: Mapped[Optional[time]] = mapped_column(
        Time,
        nullable = True
    )

    sleep_end_time: Mapped[Optional[time]] = mapped_column(
        Time,
        nullable = True
    )
    
    morning_briefing_time: Mapped[Optional[time]] = mapped_column(
        Time,
        nullable = True
    )

    evening_briefing_time: Mapped[Optional[time]] = mapped_column(
        Time,
        nullable = True
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
        back_populates = "settings"
    )

# auth_sessions(id, user_id, refresh_token_hash, status, expires_at, last_used_at, created_at, revoked_at)
class AuthSession(Base):
    # 테이블 이름
    __tablename__ = "auth_sessions"

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

    refresh_token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus),
        default = SessionStatus.ACTIVE,
        nullable = False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        nullable = False,
    )

    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "sessions"
    )

    device: Mapped["Device"] = relationship(
        "Device", 
        back_populates = "auth_sessions"
    )


