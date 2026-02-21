# schemas/expense.py

from pydantic import BaseModel, UUID4, field_validator
from typing import Optional
from datetime import datetime, date

from models.expense import ExpenseCategory


# ─── Expense ─────────────────────────────────────────────────────────────────

class ExpenseCreate(BaseModel):
    category:     ExpenseCategory
    amount:       float
    expense_date: date
    vehicle_id:   Optional[UUID4] = None
    trip_id:      Optional[UUID4] = None
    description:  Optional[str]   = None
    receipt_ref:  Optional[str]   = None

    @field_validator("amount")
    @classmethod
    def amount_not_negative(cls, v):
        if v < 0:
            raise ValueError("amount cannot be negative")
        return v


class ExpenseUpdate(BaseModel):
    category:     Optional[ExpenseCategory] = None
    amount:       Optional[float]           = None
    expense_date: Optional[date]            = None
    description:  Optional[str]             = None
    receipt_ref:  Optional[str]             = None


class ExpenseResponse(BaseModel):
    id:           UUID4
    vehicle_id:   Optional[UUID4] = None
    trip_id:      Optional[UUID4] = None
    logged_by:    Optional[UUID4] = None
    category:     ExpenseCategory
    amount:       float
    description:  Optional[str]   = None
    expense_date: date
    receipt_ref:  Optional[str]   = None
    created_at:   datetime

    class Config:
        from_attributes = True
