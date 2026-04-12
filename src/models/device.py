# devices / device_links
from src.core.database import Base  # Base import

class Device(Base):
    __tablename__ = "devices"

class DeviceLink(Base):
    __tablename__ = "device_links"