# crud/expense.py

from uuid import UUID
from sqlalchemy.orm import Session

from models.expense import Expense, ExpenseCategory
from schemas.expense import ExpenseCreate, ExpenseUpdate


def get_expense(db: Session, expense_id: UUID) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()


def get_expenses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    vehicle_id: UUID = None,
    trip_id: UUID = None,
    category: ExpenseCategory = None,
) -> list[Expense]:
    q = db.query(Expense)
    if vehicle_id:
        q = q.filter(Expense.vehicle_id == vehicle_id)
    if trip_id:
        q = q.filter(Expense.trip_id == trip_id)
    if category:
        q = q.filter(Expense.category == category)
    return q.order_by(Expense.expense_date.desc()).offset(skip).limit(limit).all()


def create_expense(
    db: Session,
    data: ExpenseCreate,
    logged_by: UUID = None,
) -> Expense:
    expense = Expense(**data.model_dump(), logged_by=logged_by)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def update_expense(
    db: Session,
    expense_id: UUID,
    data: ExpenseUpdate,
) -> Expense | None:
    expense = get_expense(db, expense_id)
    if not expense:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense
