# schemas/trip.py

from pydantic import BaseModel, UUID4, field_validator
from typing import Optional
from datetime import datetime

from models.trip import TripStatus


# ─── Trip ────────────────────────────────────────────────────────────────────

class TripCreate(BaseModel):
    vehicle_id:        UUID4
    driver_id:         UUID4
    origin:            str
    destination:       str
    cargo_weight_kg:   float
    cargo_description: Optional[str]      = None
    scheduled_at:      Optional[datetime] = None
    notes:             Optional[str]      = None

    @field_validator("cargo_weight_kg")
    @classmethod
    def weight_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("cargo_weight_kg cannot be negative")
        return v


class TripUpdate(BaseModel):
    status:          Optional[TripStatus] = None
    cancel_reason:   Optional[str]        = None
    odometer_start:  Optional[float]      = None
    odometer_end:    Optional[float]      = None
    notes:           Optional[str]        = None
    dispatched_at:   Optional[datetime]   = None
    completed_at:    Optional[datetime]   = None
    cancelled_at:    Optional[datetime]   = None


class TripResponse(BaseModel):
    id:                UUID4
    vehicle_id:        UUID4
    driver_id:         UUID4
    created_by:        Optional[UUID4] = None
    origin:            str
    destination:       str
    cargo_description: Optional[str]   = None
    cargo_weight_kg:   float
    status:            TripStatus
    scheduled_at:      Optional[datetime] = None
    dispatched_at:     Optional[datetime] = None
    completed_at:      Optional[datetime] = None
    cancelled_at:      Optional[datetime] = None
    cancel_reason:     Optional[str]      = None
    odometer_start:    Optional[float]    = None
    odometer_end:      Optional[float]    = None
    distance_km:       Optional[float]    = None   # DB-generated, read-only
    notes:             Optional[str]      = None
    created_at:        datetime

    class Config:
        from_attributes = True


# ─── TripStatusHistory ───────────────────────────────────────────────────────

class TripStatusHistoryResponse(BaseModel):
    id:         UUID4
    trip_id:    UUID4
    old_status: Optional[TripStatus] = None
    new_status: TripStatus
    notes:      Optional[str] = None
    changed_at: datetime

    class Config:
        from_attributes = True
