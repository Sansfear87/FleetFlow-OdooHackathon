# schemas/user.py

from pydantic import BaseModel, UUID4, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# ─── Role ────────────────────────────────────────────────────────────────────

class RoleResponse(BaseModel):
    id:          UUID4
    name:        str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# ─── User ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email:     EmailStr
    password:  str          # plain text — hashed in the CRUD layer
    full_name: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str]  = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id:            UUID4
    email:         str
    full_name:     str
    is_active:     bool
    last_login_at: Optional[datetime] = None
    created_at:    datetime

    class Config:
        from_attributes = True


# ─── UserRole ────────────────────────────────────────────────────────────────

class UserRoleAssign(BaseModel):
    role_id: UUID4


class UserRoleResponse(BaseModel):
    id:          UUID4
    user_id:     UUID4
    role_id:     UUID4
    assigned_at: datetime

    class Config:
        from_attributes = True
