# api/v1/vehicles.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from crud import vehicle as vehicle_crud
from schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleStatusHistoryResponse
from core.dependencies import get_current_user, require_role
from models.user import User
from models.vehicle import VehicleStatus

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get("/", response_model=list[VehicleResponse])
def list_vehicles(
    skip: int = 0,
    limit: int = 100,
    status: VehicleStatus = None,
    region: str = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return vehicle_crud.get_vehicles(db, skip=skip, limit=limit, status=status, region=region)


@router.get("/available", response_model=list[VehicleResponse])
def list_available_vehicles(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Returns only vehicles that can be assigned to a trip."""
    return vehicle_crud.get_available_vehicles(db)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    vehicle = vehicle_crud.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.post("/", response_model=VehicleResponse, status_code=201)
def create_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    return vehicle_crud.create_vehicle(db, data)


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: UUID,
    data: VehicleUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    vehicle = vehicle_crud.update_vehicle(db, vehicle_id, data)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.delete("/{vehicle_id}", status_code=204)
def retire_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    """Soft delete — sets status to 'retired'. Never hard deletes."""
    vehicle = vehicle_crud.retire_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")


@router.get("/{vehicle_id}/history", response_model=list[VehicleStatusHistoryResponse])
def get_vehicle_history(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return vehicle_crud.get_vehicle_status_history(db, vehicle_id)
