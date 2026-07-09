from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: UUID


class UserDB(UserBase):
    user_id: UUID
    hashed_password: str
