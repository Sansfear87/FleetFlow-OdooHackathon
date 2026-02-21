# models/maintenance.py

import uuid

from sqlalchemy import Column, String, Numeric, Boolean, Date, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id          = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    performed_by        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    service_type        = Column(String(200), nullable=False)
    description         = Column(Text, nullable=True)
    cost                = Column(Numeric(12, 2), nullable=False, default=0)
    start_date          = Column(Date, nullable=False)
    end_date            = Column(Date, nullable=True)
    vendor_name         = Column(String(200), nullable=True)
    odometer_at_service = Column(Numeric(12, 2), nullable=True)
    is_active           = Column(Boolean, nullable=False, default=True)
    created_at          = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at          = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenance_logs")
