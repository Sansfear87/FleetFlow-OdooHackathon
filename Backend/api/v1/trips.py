# api/v1/trips.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from database import get_db
from crud import trip as trip_crud
from schemas.trip import TripCreate, TripResponse, TripStatusHistoryResponse
from core.dependencies import get_current_user, require_role
from models.user import User
from models.trip import TripStatus

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("/", response_model=list[TripResponse])
def list_trips(
    skip: int = 0,
    limit: int = 100,
    status: TripStatus = None,
    vehicle_id: UUID = None,
    driver_id: UUID = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return trip_crud.get_trips(
        db, skip=skip, limit=limit,
        status=status, vehicle_id=vehicle_id, driver_id=driver_id
    )


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    trip = trip_crud.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("/", response_model=TripResponse, status_code=201)
def create_trip(
    data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    """
    Creates a trip. Validates:
    - Vehicle is available
    - Cargo weight does not exceed vehicle capacity
    - Driver is available and license is not expired
    """
    return trip_crud.validate_and_create_trip(db, data, created_by=current_user.id)


@router.patch("/{trip_id}/dispatch", response_model=TripResponse)
def dispatch_trip(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    """Move trip from Draft → Dispatched. Sets vehicle and driver to On Trip."""
    return trip_crud.update_trip_status(
        db, trip_id,
        new_status=TripStatus.dispatched,
        changed_by=current_user.id,
    )


@router.patch("/{trip_id}/complete", response_model=TripResponse)
def complete_trip(
    trip_id: UUID,
    odometer_end: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Move trip from Dispatched → Completed. Frees vehicle and driver."""
    return trip_crud.update_trip_status(
        db, trip_id,
        new_status=TripStatus.completed,
        changed_by=current_user.id,
        odometer_end=odometer_end,
    )


@router.patch("/{trip_id}/cancel", response_model=TripResponse)
def cancel_trip(
    trip_id: UUID,
    cancel_reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("dispatcher")),
):
    """Cancel a Draft or Dispatched trip."""
    return trip_crud.update_trip_status(
        db, trip_id,
        new_status=TripStatus.cancelled,
        changed_by=current_user.id,
        cancel_reason=cancel_reason,
    )


@router.get("/{trip_id}/history", response_model=list[TripStatusHistoryResponse])
def get_trip_history(
    trip_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return trip_crud.get_trip_status_history(db, trip_id)
