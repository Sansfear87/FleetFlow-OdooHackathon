# crud/fuel.py

from uuid import UUID
from sqlalchemy.orm import Session

from models.fuel import FuelLog
from schemas.fuel import FuelLogCreate, FuelLogUpdate


def get_fuel_log(db: Session, log_id: UUID) -> FuelLog | None:
    return db.query(FuelLog).filter(FuelLog.id == log_id).first()


def get_fuel_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    vehicle_id: UUID = None,
    trip_id: UUID = None,
) -> list[FuelLog]:
    q = db.query(FuelLog)
    if vehicle_id:
        q = q.filter(FuelLog.vehicle_id == vehicle_id)
    if trip_id:
        q = q.filter(FuelLog.trip_id == trip_id)
    return q.order_by(FuelLog.fuel_date.desc()).offset(skip).limit(limit).all()


def create_fuel_log(
    db: Session,
    data: FuelLogCreate,
    logged_by: UUID = None,
) -> FuelLog:
    log = FuelLog(**data.model_dump(), logged_by=logged_by)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def update_fuel_log(
    db: Session,
    log_id: UUID,
    data: FuelLogUpdate,
) -> FuelLog | None:
    log = get_fuel_log(db, log_id)
    if not log:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    return log
