# briefings / briefing_items
from src.core.database import Base  # Base import

class Briefing(Base):
    __tablename__ = "briefings"

class BriefingItem(Base):
    __tablename__ = "briefing_items"