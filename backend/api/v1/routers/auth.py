from typing import Annotated

from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserResponse
from services.auth import AuthService, get_auth_service

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/register")
async def read_tests(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user: UserCreate,
) -> UserResponse:
    return await auth_service.register(user)
