# models/driver.py

import uuid
import enum

from sqlalchemy import Column, String, Numeric, Integer, Date, Enum, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class DriverStatus(str, enum.Enum):
    available = "available"
    on_trip   = "on_trip"
    off_duty  = "off_duty"
    suspended = "suspended"


class Driver(Base):
    __tablename__ = "drivers"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name           = Column(String(200), nullable=False)
    employee_id         = Column(String(50), unique=True, nullable=True)
    phone               = Column(String(20), nullable=True)
    email               = Column(String(255), unique=True, nullable=True)
    license_number      = Column(String(50), nullable=False, unique=True)
    license_category    = Column(String(20), nullable=False)
    license_expiry_date = Column(Date, nullable=False)
    safety_score        = Column(Numeric(4, 2), default=100)
    status              = Column(Enum(DriverStatus), nullable=False, default=DriverStatus.available)
    trips_completed     = Column(Integer, nullable=False, default=0)
    trips_total         = Column(Integer, nullable=False, default=0)
    notes               = Column(Text, nullable=True)
    created_at          = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at          = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    trips          = relationship("Trip", back_populates="driver")
    status_history = relationship("DriverStatusHistory", back_populates="driver", cascade="all, delete-orphan")


class DriverStatusHistory(Base):
    __tablename__ = "driver_status_history"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id  = Column(UUID(as_uuid=True), ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(Enum(DriverStatus), nullable=True)
    new_status = Column(Enum(DriverStatus), nullable=False)
    reason     = Column(Text, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    driver = relationship("Driver", back_populates="status_history")
