# schemas/auth.py

from pydantic import BaseModel, UUID4
from typing import List


class TokenResponse(BaseModel):
    """Returned by POST /auth/token on successful login."""
    access_token: str
    token_type:   str = "bearer"


class TokenData(BaseModel):
    """Returned by GET /auth/me — current user profile + roles."""
    id:        UUID4
    email:     str
    full_name: str
    is_active: bool
    roles:     List[str]
