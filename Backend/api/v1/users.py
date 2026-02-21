# api/v1/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from crud import user as user_crud
from schemas.user import UserCreate, UserUpdate, UserResponse, UserRoleAssign, UserRoleResponse
from core.dependencies import get_current_user, require_role
from models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    return user_crud.get_users(db, skip=skip, limit=limit)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the currently logged-in user."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, data)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    user = user_crud.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/{user_id}/roles", response_model=UserRoleResponse, status_code=201)
def assign_role(
    user_id: UUID,
    data: UserRoleAssign,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("fleet_manager")),
):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.assign_role(db, user_id=user_id, role_id=data.role_id)
