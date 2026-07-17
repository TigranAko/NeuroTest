from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: UUID = Field(..., alias="id")
    created_at: datetime
    updated_at: datetime


class UserDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    password: str
    created_at: datetime
    updated_at: datetime
