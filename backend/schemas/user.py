from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: UUID


class UserDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    password: str
