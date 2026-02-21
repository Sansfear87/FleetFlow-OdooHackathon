# crud/maintenance.py

from uuid import UUID
from sqlalchemy.orm import Session

from models.maintenance import MaintenanceLog
from schemas.maintenance import MaintenanceCreate, MaintenanceUpdate


def get_maintenance_log(db: Session, log_id: UUID) -> MaintenanceLog | None:
    return db.query(MaintenanceLog).filter(MaintenanceLog.id == log_id).first()


def get_maintenance_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    vehicle_id: UUID = None,
    is_active: bool = None,
) -> list[MaintenanceLog]:
    q = db.query(MaintenanceLog)
    if vehicle_id:
        q = q.filter(MaintenanceLog.vehicle_id == vehicle_id)
    if is_active is not None:
        q = q.filter(MaintenanceLog.is_active == is_active)
    return q.order_by(MaintenanceLog.start_date.desc()).offset(skip).limit(limit).all()


def create_maintenance_log(
    db: Session,
    data: MaintenanceCreate,
    performed_by: UUID = None,
) -> MaintenanceLog:
    log = MaintenanceLog(**data.model_dump(), performed_by=performed_by)
    db.add(log)
    db.commit()
    db.refresh(log)
    # Note: the DB trigger automatically sets vehicle.status = 'in_shop'
    return log


def update_maintenance_log(
    db: Session,
    log_id: UUID,
    data: MaintenanceUpdate,
) -> MaintenanceLog | None:
    log = get_maintenance_log(db, log_id)
    if not log:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    # Note: if is_active set to False, DB trigger sets vehicle.status = 'available'
    return log
