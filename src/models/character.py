# character_personalities / character_personality_details
from src.core.database import Base  # Base import

class CharacterPersonality(Base):
    __tablename__ = "character_personalities"

class CharacterPersonalityDetail(Base):
    __tablename__ = "character_personality_details"