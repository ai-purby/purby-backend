# schedules / recurrence_rules / schedule_instances
from src.core.database import Base  # Base import

class Schedule(Base):
    __tablename__ = "schedules"

class RecurrenceRule(Base):
    __tablename__ = "recurrence_rules"

class ScheduleInstance(Base):
    __tablename__ = "schedule_instances"
