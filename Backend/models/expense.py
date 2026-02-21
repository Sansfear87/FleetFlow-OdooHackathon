# models/expense.py

import uuid
import enum

from sqlalchemy import Column, String, Numeric, Date, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class ExpenseCategory(str, enum.Enum):
    fuel        = "fuel"
    maintenance = "maintenance"
    toll        = "toll"
    fine        = "fine"
    insurance   = "insurance"
    other       = "other"


class Expense(Base):
    __tablename__ = "expenses"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id   = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)
    trip_id      = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=True)
    logged_by    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    category     = Column(Enum(ExpenseCategory), nullable=False)
    amount       = Column(Numeric(12, 2), nullable=False)
    description  = Column(Text, nullable=True)
    expense_date = Column(Date, nullable=False, server_default=func.current_date())
    receipt_ref  = Column(String(200), nullable=True)
    created_at   = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at   = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="expenses")
    trip    = relationship("Trip", back_populates="expenses")
