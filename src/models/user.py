# users / user_settings / auth_session
from src.core.database import Base  # Base import

class User(Base):
    __tablename__ = "users"

class UserSetting(Base):
    __tablename__ = "user_settings"

class AuthSession(Base):
    __tablename__ = "auth_sessions"
    