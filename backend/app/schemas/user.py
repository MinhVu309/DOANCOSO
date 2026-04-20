from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    display_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Mật khẩu phải có ít nhất 8 ký tự")
        return v

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username phải có ít nhất 3 ký tự")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username chỉ được chứa chữ, số, _ và -")
        return v


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    display_name: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# --- Profile & Preferences ---

from datetime import date  # noqa: E402
from typing import List  # noqa: E402
from pydantic import ConfigDict  # noqa: E402


class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    birth_date: Optional[date] = None
    timezone: Optional[str] = None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    display_name: Optional[str] = None
    email: str
    birth_date: Optional[date] = None
    timezone: str
    avatar_url: Optional[str] = None


class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    reminder_enabled: Optional[bool] = None
    reminder_time: Optional[str] = None
    reminder_days: Optional[List[str]] = None


class UserPreferencesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    theme: str
    reminder_enabled: bool
    reminder_time: Optional[str] = None
    reminder_days: List[str] = []
