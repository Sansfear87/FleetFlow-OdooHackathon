# api/v1/drivers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from crud import driver as driver_crud
from schemas.driver import DriverCreate, DriverUpdate, DriverResponse, DriverStatusHistoryResponse
from core.dependencies import get_current_user, require_role
from models.user import User
from models.driver import DriverStatus

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("/", response_model=list[DriverResponse])
def list_drivers(
    skip: int = 0,
    limit: int = 100,
    status: DriverStatus = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return driver_crud.get_drivers(db, skip=skip, limit=limit, status=status)


@router.get("/available", response_model=list[DriverResponse])
def list_available_drivers(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Returns only drivers that are available with a valid license."""
    return driver_crud.get_available_drivers(db)


@router.get("/expiring-licenses", response_model=list[DriverResponse])
def expiring_licenses(
    within_days: int = 30,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("safety_officer")),
):
    """Safety Officer alert — drivers whose license expires within N days."""
    return driver_crud.get_expiring_licenses(db, within_days=within_days)


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    driver = driver_crud.get_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.post("/", response_model=DriverResponse, status_code=201)
def create_driver(
    data: DriverCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    return driver_crud.create_driver(db, data)


@router.patch("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: UUID,
    data: DriverUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    driver = driver_crud.update_driver(db, driver_id, data)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.get("/{driver_id}/history", response_model=list[DriverStatusHistoryResponse])
def get_driver_history(
    driver_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return driver_crud.get_driver_status_history(db, driver_id)
