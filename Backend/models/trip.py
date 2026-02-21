# models/trip.py

import uuid
import enum

from sqlalchemy import Column, String, Numeric, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class TripStatus(str, enum.Enum):
    draft      = "draft"
    dispatched = "dispatched"
    completed  = "completed"
    cancelled  = "cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id       = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    driver_id        = Column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False)
    created_by       = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    origin           = Column(String(300), nullable=False)
    destination      = Column(String(300), nullable=False)
    cargo_description = Column(Text, nullable=True)
    cargo_weight_kg  = Column(Numeric(10, 2), nullable=False)
    status           = Column(Enum(TripStatus), nullable=False, default=TripStatus.draft)
    scheduled_at     = Column(TIMESTAMP(timezone=True), nullable=True)
    dispatched_at    = Column(TIMESTAMP(timezone=True), nullable=True)
    completed_at     = Column(TIMESTAMP(timezone=True), nullable=True)
    cancelled_at     = Column(TIMESTAMP(timezone=True), nullable=True)
    cancel_reason    = Column(Text, nullable=True)
    odometer_start   = Column(Numeric(12, 2), nullable=True)
    odometer_end     = Column(Numeric(12, 2), nullable=True)
    # distance_km is a GENERATED column in the DB — do NOT write to it from Python
    # SQLAlchemy will read it automatically after commit
    notes            = Column(Text, nullable=True)
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle        = relationship("Vehicle", back_populates="trips")
    driver         = relationship("Driver", back_populates="trips")
    status_history = relationship("TripStatusHistory", back_populates="trip", cascade="all, delete-orphan")
    fuel_logs      = relationship("FuelLog", back_populates="trip")
    expenses       = relationship("Expense", back_populates="trip")


class TripStatusHistory(Base):
    __tablename__ = "trip_status_history"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id    = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(Enum(TripStatus), nullable=True)
    new_status = Column(Enum(TripStatus), nullable=False)
    notes      = Column(Text, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    trip = relationship("Trip", back_populates="status_history")
