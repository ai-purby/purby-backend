# character_personalities / character_personality_details
from src.core.database import Base  # Base import
import uuid
from sqlalchemy import String, text, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

# character_personalities(id, name, description)
class CharacterPersonality(Base):
    # 테이블 이름
    __tablename__ = "character_personalities"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    name: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    # 관계 지정
    character_personality_details: Mapped[list["CharacterPersonalityDetail"]] = relationship(
        "CharacterPersonalityDetail",
        back_populates="character_personality",
        cascade = "all, delete-orphan"
    )

# character_personality_details(id, personality_id, characteristic)
class CharacterPersonalityDetail(Base):
    # 테이블 이름
    __tablename__ = "character_personality_details"

    # 식별자
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    personality_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("character_personalities.id", ondelete="CASCADE")
    )

    characteristic: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    # 관계 지정
    character_personality: Mapped["CharacterPersonality"] = relationship(
        "CharacterPersonality",
        back_populates="character_personality_details",
    )

