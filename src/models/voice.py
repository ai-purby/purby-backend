# voice_sessions / voice_commands / intent_codes / conversation_events
from src.core.database import Base  # Base import

class VoiceSession(Base):
    __tablename__ = "voice_sessions"

class VoiceCommand(Base):
    __tablename__ = "voice_commands"

class IntentCode(Base):
    __tablename__ = "intent_codes"

class ConversationEvent(Base):
    __tablename__ = "conversation_events"

