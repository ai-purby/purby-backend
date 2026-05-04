# briefings / briefing_items
from src.core.database import Base  # Base import
import enum, uuid
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import DateTime, text, ForeignKey, Integer, Enum, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from src.models.user import User

# Enum Class
class BriefingTime(str, enum.Enum):
    MORNING = "morning"
    EVENING = "evening"

# briefings(id, user_id, target_date, summary, time_of_day, tomorrow_plan_summary, created_at)
class Briefing(Base):
    # 테이블 이름
    __tablename__ = "briefings"

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

    target_date: Mapped[date] = mapped_column(
        Date,
        nullable= False
    )

    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    time_of_day: Mapped[BriefingTime] = mapped_column(
        Enum(BriefingTime),
        nullable=False
    )

    tomorrow_plan_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    # 관계 지정
    user: Mapped["User"] = relationship(
        "User", 
        back_populates = "briefings"
    )

    briefing_items: Mapped[list["BriefingItem"]] = relationship(
        "BriefingItem",
        back_populates= "briefing",
        cascade = "all, delete-orphan"
    )


# briefing_items(id, briefing_id, display_order, question, answer, created_at)
class BriefingItem(Base):
    # 테이블 이름
    __tablename__ = "briefing_items"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    briefing_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("briefings.id", ondelete = "CASCADE"),
        nullable = False
    )

    display_order: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable= True
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable= False
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable= False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    # 관계 지정
    briefing: Mapped["Briefing"] = relationship(
        "Briefing", 
        back_populates = "briefing_items"
    )