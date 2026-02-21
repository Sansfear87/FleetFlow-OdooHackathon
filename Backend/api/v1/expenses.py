# api/v1/expenses.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from database import get_db
from crud import expense as expense_crud
from schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from core.dependencies import get_current_user, require_role
from models.user import User
from models.expense import ExpenseCategory

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[UUID] = None,
    trip_id: Optional[UUID] = None,
    category: Optional[ExpenseCategory] = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return expense_crud.get_expenses(
        db, skip=skip, limit=limit,
        vehicle_id=vehicle_id, trip_id=trip_id, category=category
    )


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    expense = expense_crud.get_expense(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return expense_crud.create_expense(db, data, logged_by=current_user.id)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: UUID,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("financial_analyst")),
):
    expense = expense_crud.update_expense(db, expense_id, data)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense
