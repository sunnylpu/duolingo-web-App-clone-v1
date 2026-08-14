from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.modules.user.schemas import UserResponse


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=6, max_length=128)
    display_name: Optional[str] = None


class LoginRequest(BaseModel):
    email_or_username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)
