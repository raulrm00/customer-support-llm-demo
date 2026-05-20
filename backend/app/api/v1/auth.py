from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema, UserCreate, LoginRequest

router = APIRouter()
settings = get_settings()

@router.post("/register", response_model=UserSchema)
def register(
    db: Annotated[Session, Depends(get_db)],
    user_in: UserCreate,
) -> UserSchema:
    """Register a new user."""
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    new_user = User(
        email=user_in.email,
        password_hash=security.get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_admin=user_in.is_admin,
        daily_limit_seconds=settings.default_daily_limit_seconds,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

@router.post("/login", response_model=Token)
def login(
    db: Annotated[Session, Depends(get_db)],
    login_data: LoginRequest,
) -> Token:
    """Standard login with JSON body."""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not security.verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> UserSchema:
    """Get current user."""
    return current_user
