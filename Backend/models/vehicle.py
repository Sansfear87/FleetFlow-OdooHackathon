# models/vehicle.py

import uuid
import enum

from sqlalchemy import Column, String, Numeric, Enum, Text, Date, TIMESTAMP, SmallInteger, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class VehicleStatus(str, enum.Enum):
    available = "available"
    on_trip   = "on_trip"
    in_shop   = "in_shop"
    retired   = "retired"


class VehicleType(str, enum.Enum):
    truck = "truck"
    van   = "van"
    bike  = "bike"
    car   = "car"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name             = Column(String(100), nullable=False)
    license_plate    = Column(String(20), nullable=False, unique=True)
    vehicle_type     = Column(Enum(VehicleType), nullable=False)
    make             = Column(String(100), nullable=True)
    model            = Column(String(100), nullable=True)
    year             = Column(SmallInteger, nullable=True)
    max_capacity_kg  = Column(Numeric(10, 2), nullable=False)
    odometer_km      = Column(Numeric(12, 2), default=0)
    status           = Column(Enum(VehicleStatus), default=VehicleStatus.available)
    acquisition_cost = Column(Numeric(12, 2), nullable=True)
    acquired_at      = Column(Date, nullable=True)
    region           = Column(String(100), nullable=True)
    notes            = Column(Text, nullable=True)
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    trips            = relationship("Trip", back_populates="vehicle")
    maintenance_logs = relationship("MaintenanceLog", back_populates="vehicle")
    fuel_logs        = relationship("FuelLog", back_populates="vehicle")
    expenses         = relationship("Expense", back_populates="vehicle")
    status_history   = relationship("VehicleStatusHistory", back_populates="vehicle", cascade="all, delete-orphan")


class VehicleStatusHistory(Base):
    __tablename__ = "vehicle_status_history"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(Enum(VehicleStatus), nullable=True)
    new_status = Column(Enum(VehicleStatus), nullable=False)
    reason     = Column(Text, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="status_history")
