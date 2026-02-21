# api/v1/auth.py

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from crud.user import get_user_by_email
from core.security import verify_password, create_access_token
from core.dependencies import get_current_user
from schemas.auth import TokenResponse, TokenData
from models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2-compatible login endpoint.
    Accepts: username (email) + password as form data.
    Returns: JWT access token.
    """
    # 1. Look up user by email
    user = get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Verify password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Block inactive users
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Contact your administrator.",
        )

    # 4. Collect roles for the token payload
    roles = [ur.role.name for ur in user.user_roles]

    # 5. Mint JWT
    token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "roles": roles,
    })

    # 6. Update last_login_at
    user.last_login_at = datetime.utcnow()
    db.commit()

    return TokenResponse(access_token=token, token_type="bearer")


@router.post("/logout")
def logout(_user: User = Depends(get_current_user)):
    """
    Stateless logout — instructs the client to discard the token.
    Since JWTs are stateless, revocation is handled client-side.
    For production token blacklisting, use Redis TTL on the JTI claim.
    """
    return {"message": "Logged out successfully. Discard your token."}


@router.get("/me", response_model=TokenData)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns the currently authenticated user's profile + roles.
    Useful for the frontend to bootstrap UI based on role.
    """
    return TokenData(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        roles=[ur.role.name for ur in current_user.user_roles],
    )
