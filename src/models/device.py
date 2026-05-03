# devices / device_links
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from src.models.user import User, AuthSession
    from src.models.system import SystemLog

# Enum Class
class DeviceType(str, enum.Enum) :
    DESKTOP = "desktop"
    MOBILE = "mobile"

class DevicePlatform(str, enum.Enum) :
    LINUX = "linux"
    IOS = "iOS"
    ANDROID = "android"

class DeviceLinkStatus(str, enum.Enum) :
    LINKED = "linked"
    REVOKED = "revoked"


# devices(id, user_id, device_type, platform, app_version, os_version, created_at, updated_at)
class Device(Base):
    # 테이블 이름
    __tablename__ = "devices"

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

    device_type: Mapped[DeviceType] = mapped_column(
        Enum(DeviceType),
        default = DeviceType.DESKTOP,
        nullable = False
    )

    platform: Mapped[DevicePlatform | None] = mapped_column(
        Enum(DevicePlatform),
        nullable=True
    )

    app_version: Mapped[Optional[str]] = mapped_column(
        String(20),
        default="1.0.0",
        nullable=True
    )

    os_version: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
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
        back_populates = "devices"
    )

    desktop_links: Mapped[list["DeviceLink"]] = relationship(
        "DeviceLink", 
        back_populates = "desktop_device",
        cascade = "all, delete-orphan"
    )

    mobile_links: Mapped[list["DeviceLink"]] = relationship(
        "DeviceLink", 
        back_populates = "mobile_device",
        cascade = "all, delete-orphan"
    )

    auth_sessions: Mapped[list["AuthSession"]] = relationship(
        "AuthSession", 
        back_populates = "device",
        cascade = "all, delete-orphan"
    )

    system_logs: Mapped[list["SystemLog"]] = relationship(
        "SystemLog",
        back_populates= "device",
        cascade= "all, delete-orphan"
    )

# device_links(id, desktop_device_id, mobile_device_id, status, linked_at, revoked_at)
class DeviceLink(Base):
    # 테이블 이름
    __tablename__ = "device_links"

        # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    desktop_device_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable = True
    )

    mobile_device_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable = True
    )

    status: Mapped[DeviceLinkStatus] = mapped_column(
        Enum(DeviceLinkStatus),
        default = DeviceLinkStatus.LINKED,
        nullable = False
    )

    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"), 
        nullable = False
    )

    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    # 관계 지정
    desktop_device: Mapped[Optional["Device"]] = relationship(
        "Device", 
        foreign_keys=[desktop_device_id],
        back_populates = "desktop_links"
    )

    mobile_device: Mapped[Optional["Device"]] = relationship(
        "Device", 
        foreign_keys=[mobile_device_id],
        back_populates = "mobile_links"
    )

