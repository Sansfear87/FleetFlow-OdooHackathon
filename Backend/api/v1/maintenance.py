# api/v1/maintenance.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from database import get_db
from crud import maintenance as maintenance_crud
from schemas.maintenance import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from core.dependencies import get_current_user, require_role
from models.user import User

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("/", response_model=list[MaintenanceResponse])
def list_maintenance_logs(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[UUID] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return maintenance_crud.get_maintenance_logs(
        db, skip=skip, limit=limit,
        vehicle_id=vehicle_id, is_active=is_active
    )


@router.get("/{log_id}", response_model=MaintenanceResponse)
def get_maintenance_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    log = maintenance_crud.get_maintenance_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return log


@router.post("/", response_model=MaintenanceResponse, status_code=201)
def create_maintenance_log(
    data: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("fleet_manager")),
):
    """
    Creates a maintenance log.
    DB trigger automatically sets vehicle status to 'in_shop'.
    """
    return maintenance_crud.create_maintenance_log(db, data, performed_by=current_user.id)


@router.patch("/{log_id}", response_model=MaintenanceResponse)
def update_maintenance_log(
    log_id: UUID,
    data: MaintenanceUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    """
    Set is_active=false to mark maintenance complete.
    DB trigger automatically sets vehicle status back to 'available'.
    """
    log = maintenance_crud.update_maintenance_log(db, log_id, data)
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    return log
