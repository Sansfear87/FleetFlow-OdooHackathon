# schemas/maintenance.py

from pydantic import BaseModel, UUID4, field_validator
from typing import Optional
from datetime import datetime, date


# ─── MaintenanceLog ──────────────────────────────────────────────────────────

class MaintenanceCreate(BaseModel):
    vehicle_id:          UUID4
    service_type:        str
    start_date:          date
    cost:                float             = 0
    description:         Optional[str]    = None
    end_date:            Optional[date]   = None
    vendor_name:         Optional[str]    = None
    odometer_at_service: Optional[float]  = None

    @field_validator("cost")
    @classmethod
    def cost_not_negative(cls, v):
        if v < 0:
            raise ValueError("cost cannot be negative")
        return v


class MaintenanceUpdate(BaseModel):
    service_type:        Optional[str]   = None
    description:         Optional[str]   = None
    cost:                Optional[float] = None
    end_date:            Optional[date]  = None
    vendor_name:         Optional[str]   = None
    odometer_at_service: Optional[float] = None
    is_active:           Optional[bool]  = None  # set False to mark complete → frees vehicle


class MaintenanceResponse(BaseModel):
    id:                  UUID4
    vehicle_id:          UUID4
    performed_by:        Optional[UUID4] = None
    service_type:        str
    description:         Optional[str]   = None
    cost:                float
    start_date:          date
    end_date:            Optional[date]  = None
    vendor_name:         Optional[str]   = None
    odometer_at_service: Optional[float] = None
    is_active:           bool
    created_at:          datetime

    class Config:
        from_attributes = True
