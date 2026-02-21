# schemas/fuel.py

from pydantic import BaseModel, UUID4, field_validator
from typing import Optional
from datetime import datetime, date


# ─── FuelLog ─────────────────────────────────────────────────────────────────

class FuelLogCreate(BaseModel):
    vehicle_id:       UUID4
    liters:           float
    cost_per_liter:   float
    fuel_date:        date
    trip_id:          Optional[UUID4] = None
    odometer_at_fill: Optional[float] = None
    station_name:     Optional[str]   = None
    notes:            Optional[str]   = None

    @field_validator("liters")
    @classmethod
    def liters_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("liters must be greater than 0")
        return v

    @field_validator("cost_per_liter")
    @classmethod
    def rate_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("cost_per_liter must be greater than 0")
        return v


class FuelLogUpdate(BaseModel):
    liters:           Optional[float] = None
    cost_per_liter:   Optional[float] = None
    fuel_date:        Optional[date]  = None
    odometer_at_fill: Optional[float] = None
    station_name:     Optional[str]   = None
    notes:            Optional[str]   = None


class FuelLogResponse(BaseModel):
    id:               UUID4
    vehicle_id:       UUID4
    trip_id:          Optional[UUID4]  = None
    logged_by:        Optional[UUID4]  = None
    liters:           float
    cost_per_liter:   float
    total_cost:       Optional[float]  = None   # DB-generated, read-only
    odometer_at_fill: Optional[float]  = None
    fuel_date:        date
    station_name:     Optional[str]    = None
    notes:            Optional[str]    = None
    created_at:       datetime

    class Config:
        from_attributes = True
