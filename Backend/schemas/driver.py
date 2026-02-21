# schemas/driver.py

from pydantic import BaseModel, UUID4, EmailStr, field_validator
from typing import Optional
from datetime import datetime, date

from models.driver import DriverStatus


# ─── Driver ──────────────────────────────────────────────────────────────────

class DriverCreate(BaseModel):
    full_name:           str
    license_number:      str
    license_category:    str
    license_expiry_date: date
    employee_id:         Optional[str]      = None
    phone:               Optional[str]      = None
    email:               Optional[EmailStr] = None
    notes:               Optional[str]      = None

    @field_validator("license_expiry_date")
    @classmethod
    def expiry_must_be_future(cls, v):
        if v < date.today():
            raise ValueError("license_expiry_date is already in the past")
        return v


class DriverUpdate(BaseModel):
    full_name:           Optional[str]          = None
    phone:               Optional[str]          = None
    email:               Optional[EmailStr]     = None
    status:              Optional[DriverStatus] = None
    license_expiry_date: Optional[date]         = None
    safety_score:        Optional[float]        = None
    notes:               Optional[str]          = None

    @field_validator("safety_score")
    @classmethod
    def score_in_range(cls, v):
        if v is not None and not (0 <= v <= 100):
            raise ValueError("safety_score must be between 0 and 100")
        return v


class DriverResponse(BaseModel):
    id:                  UUID4
    full_name:           str
    employee_id:         Optional[str]  = None
    phone:               Optional[str]  = None
    email:               Optional[str]  = None
    license_number:      str
    license_category:    str
    license_expiry_date: date
    safety_score:        Optional[float] = None
    status:              DriverStatus
    trips_completed:     int
    trips_total:         int
    notes:               Optional[str]  = None
    created_at:          datetime

    class Config:
        from_attributes = True


# ─── DriverStatusHistory ─────────────────────────────────────────────────────

class DriverStatusHistoryResponse(BaseModel):
    id:         UUID4
    driver_id:  UUID4
    old_status: Optional[DriverStatus] = None
    new_status: DriverStatus
    reason:     Optional[str]  = None
    changed_at: datetime

    class Config:
        from_attributes = True
