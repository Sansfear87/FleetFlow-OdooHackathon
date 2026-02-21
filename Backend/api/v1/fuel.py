# api/v1/fuel.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from database import get_db
from crud import fuel as fuel_crud
from schemas.fuel import FuelLogCreate, FuelLogUpdate, FuelLogResponse
from core.dependencies import get_current_user, require_role
from models.user import User

router = APIRouter(prefix="/fuel", tags=["Fuel Logs"])


@router.get("/", response_model=list[FuelLogResponse])
def list_fuel_logs(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[UUID] = None,
    trip_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return fuel_crud.get_fuel_logs(
        db, skip=skip, limit=limit,
        vehicle_id=vehicle_id, trip_id=trip_id
    )


@router.get("/{log_id}", response_model=FuelLogResponse)
def get_fuel_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    log = fuel_crud.get_fuel_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Fuel log not found")
    return log


@router.post("/", response_model=FuelLogResponse, status_code=201)
def create_fuel_log(
    data: FuelLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return fuel_crud.create_fuel_log(db, data, logged_by=current_user.id)


@router.patch("/{log_id}", response_model=FuelLogResponse)
def update_fuel_log(
    log_id: UUID,
    data: FuelLogUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    log = fuel_crud.update_fuel_log(db, log_id, data)
    if not log:
        raise HTTPException(status_code=404, detail="Fuel log not found")
    return log
