# crud/trip.py

from uuid import UUID
from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.trip import Trip, TripStatus, TripStatusHistory
from models.vehicle import Vehicle, VehicleStatus
from models.driver import Driver, DriverStatus
from schemas.trip import TripCreate, TripUpdate


def get_trip(db: Session, trip_id: UUID) -> Trip | None:
    return db.query(Trip).filter(Trip.id == trip_id).first()


def get_trips(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: TripStatus = None,
    vehicle_id: UUID = None,
    driver_id: UUID = None,
) -> list[Trip]:
    q = db.query(Trip)
    if status:
        q = q.filter(Trip.status == status)
    if vehicle_id:
        q = q.filter(Trip.vehicle_id == vehicle_id)
    if driver_id:
        q = q.filter(Trip.driver_id == driver_id)
    return q.order_by(Trip.created_at.desc()).offset(skip).limit(limit).all()


def validate_and_create_trip(
    db: Session,
    data: TripCreate,
    created_by: UUID = None,
) -> Trip:
    # 1. Vehicle must exist and be available
    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if vehicle.status != VehicleStatus.available:
        raise HTTPException(
            status_code=400,
            detail=f"Vehicle is '{vehicle.status.value}', not available for dispatch",
        )

    # 2. Cargo weight must not exceed vehicle capacity
    if data.cargo_weight_kg > vehicle.max_capacity_kg:
        raise HTTPException(
            status_code=400,
            detail=f"Cargo {data.cargo_weight_kg}kg exceeds vehicle capacity {vehicle.max_capacity_kg}kg",
        )

    # 3. Driver must exist, be available, and have a valid license
    driver = db.query(Driver).filter(Driver.id == data.driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    if driver.status != DriverStatus.available:
        raise HTTPException(
            status_code=400,
            detail=f"Driver is '{driver.status.value}', not available",
        )
    if driver.license_expiry_date < date.today():
        raise HTTPException(
            status_code=400,
            detail=f"Driver license expired on {driver.license_expiry_date}",
        )

    # 4. All checks passed — create the trip
    trip = Trip(**data.model_dump(), created_by=created_by)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def update_trip_status(
    db: Session,
    trip_id: UUID,
    new_status: TripStatus,
    changed_by: UUID = None,
    notes: str = None,
    odometer_end: float = None,
    cancel_reason: str = None,
) -> Trip:
    trip = get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    old_status = trip.status

    # Guard invalid transitions
    allowed = {
        TripStatus.draft:      [TripStatus.dispatched, TripStatus.cancelled],
        TripStatus.dispatched: [TripStatus.completed, TripStatus.cancelled],
        TripStatus.completed:  [],
        TripStatus.cancelled:  [],
    }
    if new_status not in allowed[old_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition trip from '{old_status.value}' to '{new_status.value}'",
        )

    # Apply timestamps
    trip.status = new_status
    if new_status == TripStatus.dispatched:
        trip.dispatched_at = datetime.utcnow()
    elif new_status == TripStatus.completed:
        trip.completed_at = datetime.utcnow()
        if odometer_end:
            trip.odometer_end = odometer_end
    elif new_status == TripStatus.cancelled:
        trip.cancelled_at = datetime.utcnow()
        trip.cancel_reason = cancel_reason

    db.commit()
    db.refresh(trip)

    # Record history
    history = TripStatusHistory(
        trip_id=trip_id,
        old_status=old_status,
        new_status=new_status,
        changed_by=changed_by,
        notes=notes,
    )
    db.add(history)
    db.commit()

    return trip


def get_trip_status_history(db: Session, trip_id: UUID) -> list[TripStatusHistory]:
    return (
        db.query(TripStatusHistory)
        .filter(TripStatusHistory.trip_id == trip_id)
        .order_by(TripStatusHistory.changed_at.desc())
        .all()
    )
