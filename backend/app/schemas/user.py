from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Shared user properties."""
    email: EmailStr | None = None
    is_active: bool | None = True
    is_admin: bool = False


class UserCreate(UserBase):
    """Properties to receive via API on user creation."""
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """Properties to receive via API on user update."""
    password: str | None = None


class User(UserBase):
    """Properties to return via API."""
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    daily_usage_seconds: float
    daily_limit_seconds: float

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Request body for login."""
    email: EmailStr
    password: str
