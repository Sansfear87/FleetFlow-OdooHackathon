# models/fuel.py

import uuid

from sqlalchemy import Column, String, Numeric, Date, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id       = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    trip_id          = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=True)
    logged_by        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    liters           = Column(Numeric(8, 3), nullable=False)
    cost_per_liter   = Column(Numeric(8, 4), nullable=False)
    # total_cost is a GENERATED column in the DB — do NOT write to it from Python
    # SQLAlchemy will read it automatically after commit
    odometer_at_fill = Column(Numeric(12, 2), nullable=True)
    fuel_date        = Column(Date, nullable=False, server_default=func.current_date())
    station_name     = Column(String(200), nullable=True)
    notes            = Column(Text, nullable=True)
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="fuel_logs")
    trip    = relationship("Trip", back_populates="fuel_logs")
