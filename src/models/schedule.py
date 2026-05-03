# schedules / recurrence_rules / schedule_instances
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime, time
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, text, ForeignKey, Time, Integer, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from src.models.user import User

# Enum Class
class ScheduleRepeatType(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly" 

# schedules(id, user_id, title, is_all_day, location, is_recurring)
class Schedule(Base):
    # 테이블 이름
    __tablename__ = "schedules"

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

    title: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    is_all_day: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True
    )

    is_recurring: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "schedules"
    )

    recurrence_rules: Mapped[list["RecurrenceRule"]] = relationship(
        "RecurrenceRule",
        back_populates= "schedule",
        cascade= "all, delete-orphan"
    )

    schedule_instances: Mapped[list["ScheduleInstance"]] = relationship(
        "ScheduleInstance",
        back_populates= "schedule",
        cascade= "all, delete-orphan"
    )

# recurrence_rules(id, schedule_id, repeat_type, repeat_interval, repeat_days, repeat_month_day, end_date, created_at, updated_at)
class RecurrenceRule(Base):
    # 테이블 이름
    __tablename__ = "recurrence_rules"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedules.id", ondelete = "CASCADE"),
        nullable = False
    )

    repeat_type: Mapped[ScheduleRepeatType] = mapped_column(
        Enum(ScheduleRepeatType),
        nullable = False
    )

    repeat_interval: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    repeat_days: Mapped[Optional[str]] = mapped_column(
        String(5),
        nullable=True
    )

    repeat_month_day: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    end_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone = True),
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

    schedule: Mapped["Schedule"] = relationship(
        "Schedule", 
        back_populates = "recurrence_rules"
    )
    

# schedule_instances(id, schedule_id, start_datetime, end_datetime, is_success)
class ScheduleInstance(Base):
    # 테이블 이름
    __tablename__ = "schedule_instances"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("schedules.id", ondelete = "CASCADE"),
        nullable = False
    )

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        nullable = False
    )   

    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        nullable = False
    )   

    is_success: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    schedule: Mapped["Schedule"] = relationship(
        "Schedule", 
        back_populates = "schedule_instances"
    )
