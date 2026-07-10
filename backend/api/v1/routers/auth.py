from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserResponse
from services.auth import AuthService, get_auth_service
from services.jwt import get_current_user_id

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user: UserCreate,
) -> UserResponse:
    return await auth_service.register(user)


@router.post("/login")
async def login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await auth_service.login(response, form_data)


@router.post("/refresh")
async def refresh(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: Request,
    response: Response,
):
    return await auth_service.refresh(request, response)


@router.get("/myid")
async def what_my_id(user_id: Annotated[UUID, Depends(get_current_user_id)]):
    return {"user_id": user_id}
