# notifications / system_logs
from src.core.database import Base  # Base import

class Notification(Base):
    __tablename__ = "notifications"

class SystemLog(Base):
    __tablename__ = "system_logs"