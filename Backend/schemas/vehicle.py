# schemas/vehicle.py

from pydantic import BaseModel, UUID4, field_validator
from typing import Optional
from datetime import datetime

from models.vehicle import VehicleStatus, VehicleType


# ─── Vehicle ─────────────────────────────────────────────────────────────────

class VehicleCreate(BaseModel):
    name:             str
    license_plate:    str
    vehicle_type:     VehicleType
    max_capacity_kg:  float
    make:             Optional[str]   = None
    model:            Optional[str]   = None
    year:             Optional[int]   = None
    acquisition_cost: Optional[float] = None
    acquired_at:      Optional[str]   = None   # "YYYY-MM-DD"
    region:           Optional[str]   = None
    notes:            Optional[str]   = None

    @field_validator("max_capacity_kg")
    @classmethod
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("max_capacity_kg must be greater than 0")
        return v

    @field_validator("year")
    @classmethod
    def year_in_range(cls, v):
        if v is not None and not (1990 <= v <= 2100):
            raise ValueError("year must be between 1990 and 2100")
        return v


class VehicleUpdate(BaseModel):
    name:             Optional[str]          = None
    status:           Optional[VehicleStatus] = None
    make:             Optional[str]          = None
    model:            Optional[str]          = None
    year:             Optional[int]          = None
    odometer_km:      Optional[float]        = None
    acquisition_cost: Optional[float]        = None
    region:           Optional[str]          = None
    notes:            Optional[str]          = None


class VehicleResponse(BaseModel):
    id:               UUID4
    name:             str
    license_plate:    str
    vehicle_type:     VehicleType
    make:             Optional[str]   = None
    model:            Optional[str]   = None
    year:             Optional[int]   = None
    max_capacity_kg:  float
    odometer_km:      float
    status:           VehicleStatus
    acquisition_cost: Optional[float] = None
    region:           Optional[str]   = None
    notes:            Optional[str]   = None
    created_at:       datetime

    class Config:
        from_attributes = True


# ─── VehicleStatusHistory ────────────────────────────────────────────────────

class VehicleStatusHistoryResponse(BaseModel):
    id:         UUID4
    vehicle_id: UUID4
    old_status: Optional[VehicleStatus] = None
    new_status: VehicleStatus
    reason:     Optional[str]  = None
    changed_at: datetime

    class Config:
        from_attributes = True
