# crud/driver.py

from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session

from models.driver import Driver, DriverStatus, DriverStatusHistory
from schemas.driver import DriverCreate, DriverUpdate


def get_driver(db: Session, driver_id: UUID) -> Driver | None:
    return db.query(Driver).filter(Driver.id == driver_id).first()


def get_drivers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: DriverStatus = None,
) -> list[Driver]:
    q = db.query(Driver)
    if status:
        q = q.filter(Driver.status == status)
    return q.offset(skip).limit(limit).all()


def get_available_drivers(db: Session) -> list[Driver]:
    """Drivers that are available AND have a valid (non-expired) license."""
    return (
        db.query(Driver)
        .filter(
            Driver.status == DriverStatus.available,
            Driver.license_expiry_date >= date.today(),
        )
        .all()
    )


def get_expiring_licenses(db: Session, within_days: int = 30) -> list[Driver]:
    """Drivers whose license expires within N days — for Safety Officer alerts."""
    from datetime import timedelta
    cutoff = date.today() + timedelta(days=within_days)
    return (
        db.query(Driver)
        .filter(Driver.license_expiry_date <= cutoff)
        .order_by(Driver.license_expiry_date)
        .all()
    )


def create_driver(db: Session, data: DriverCreate) -> Driver:
    driver = Driver(**data.model_dump())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def update_driver(db: Session, driver_id: UUID, data: DriverUpdate) -> Driver | None:
    driver = get_driver(db, driver_id)
    if not driver:
        return None
    old_status = driver.status
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(driver, key, value)
    db.commit()
    db.refresh(driver)

    # Record status change if it changed
    if data.status and data.status != old_status:
        history = DriverStatusHistory(
            driver_id=driver_id,
            old_status=old_status,
            new_status=data.status,
        )
        db.add(history)
        db.commit()

    return driver


def get_driver_status_history(db: Session, driver_id: UUID) -> list[DriverStatusHistory]:
    return (
        db.query(DriverStatusHistory)
        .filter(DriverStatusHistory.driver_id == driver_id)
        .order_by(DriverStatusHistory.changed_at.desc())
        .all()
    )
