from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
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


@router.post("/login")
async def login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> UserResponse:
    return await auth_service.register(response, form_data)
