# voice_sessions / voice_commands / conversation_events
from src.core.database import Base  # Base import

class VoiceSession(Base):
    __tablename__ = "voice_sessions"

class VoiceCommand(Base):
    __tablename__ = "voice_commands"

class ConversationEvent(Base):
    __tablename__ = "conversation_events"

