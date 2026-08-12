from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
