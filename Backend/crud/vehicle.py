# crud/vehicle.py

from uuid import UUID
from sqlalchemy.orm import Session

from models.vehicle import Vehicle, VehicleStatus, VehicleStatusHistory
from schemas.vehicle import VehicleCreate, VehicleUpdate


def get_vehicle(db: Session, vehicle_id: UUID) -> Vehicle | None:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def get_vehicles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: VehicleStatus = None,
    region: str = None,
) -> list[Vehicle]:
    q = db.query(Vehicle)
    if status:
        q = q.filter(Vehicle.status == status)
    if region:
        q = q.filter(Vehicle.region == region)
    return q.offset(skip).limit(limit).all()


def get_available_vehicles(db: Session) -> list[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.status == VehicleStatus.available).all()


def create_vehicle(db: Session, data: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(**data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(db: Session, vehicle_id: UUID, data: VehicleUpdate) -> Vehicle | None:
    vehicle = get_vehicle(db, vehicle_id)
    if not vehicle:
        return None
    old_status = vehicle.status
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)

    # Record status change if it changed
    if data.status and data.status != old_status:
        history = VehicleStatusHistory(
            vehicle_id=vehicle_id,
            old_status=old_status,
            new_status=data.status,
        )
        db.add(history)
        db.commit()

    return vehicle


def retire_vehicle(db: Session, vehicle_id: UUID) -> Vehicle | None:
    vehicle = get_vehicle(db, vehicle_id)
    if not vehicle:
        return None
    old_status = vehicle.status
    vehicle.status = VehicleStatus.retired
    db.commit()
    db.refresh(vehicle)

    history = VehicleStatusHistory(
        vehicle_id=vehicle_id,
        old_status=old_status,
        new_status=VehicleStatus.retired,
        reason="Manually retired",
    )
    db.add(history)
    db.commit()
    return vehicle


def get_vehicle_status_history(db: Session, vehicle_id: UUID) -> list[VehicleStatusHistory]:
    return (
        db.query(VehicleStatusHistory)
        .filter(VehicleStatusHistory.vehicle_id == vehicle_id)
        .order_by(VehicleStatusHistory.changed_at.desc())
        .all()
    )
