from typing import Annotated
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from core.database import get_db
from core.settings import auth_settings as settings
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from repositories.user import UserRepository
from schemas.user import UserCreate, UserDB, UserResponse
from services.jwt import jwt_service
from sqlalchemy.ext.asyncio import AsyncSession

ph = PasswordHasher()


class AuthService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.users_repo = UserRepository(db)

    async def register(
        self,
        user: UserCreate,
    ) -> UserResponse:
        if await self.users_repo.get_by_username(user.username) is not None:
            raise HTTPException(
                401,
                "User with this username already created, please change username",
            )  # TODO: change description
        hashed_password = ph.hash(user.password)
        user.password = hashed_password
        user_id = await self.users_repo.add_one(user)
        await self.db.commit()
        return UserResponse(username=user.username, user_id=user_id)

    async def login(
        self,
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends],
    ):
        user = await self.users_repo.get_by_username(form_data.username)
        if user is None:
            raise HTTPException(401, "User Not Found")
        user = UserDB.model_validate(user)
        try:
            ph.verify(user.password, form_data.password)
        except VerificationError:
            raise HTTPException(401, "User Not Found")

        access = jwt_service.create_access_token(user.id)
        refresh = jwt_service.create_refresh_token(user.id)

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.auth_refresh_expire_days * 86400,
        )
        # response.set_cookie(
        #     key="access_token",
        #     value=access,
        #     httponly=True,
        #     secure=True,
        #     samesite="strict",
        #     max_age=settings.auth_access_expire_minutes * 60,
        # )
        return {"access_token": access, "token_type": "Bearer"}
        # return UserResponse(
        #     username=user.username,
        #     user_id=user.user_id,
        # )

    async def refresh(
        self,
        request: Request,
        response: Response,
    ):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(401, detail="Refresh token missing")

        user_id = jwt_service.verify_token(refresh_token, allowed_types=["refresh"])
        if user_id is None:
            # Удаляем битый cookie
            response.delete_cookie("refresh_token")
            raise HTTPException(401, detail="Invalid or expired refresh token")

        # Ротация: выдаём новую пару (старый refresh продолжает жить до истечения, но клиент его заменит)
        new_access = jwt_service.create_access_token(user_id)
        new_refresh = jwt_service.create_refresh_token(user_id)
        response.set_cookie(
            key="refresh_token",
            value=new_refresh,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.auth_refresh_expire_days * 86400,
        )
        return {"access_token": new_access, "token_type": "Bearer"}

    async def logout(
        self,
        response: Response,
        user_id: UUID,
    ):
        response.delete_cookie("refresh_token")
        # Access сам истечёт через 15 минут
        return {"ok": True}

    async def me(
        self,
        user_id,
    ):
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(401, "User Not Found")
        return UserResponse(username=user.username, user_id=user.id)


def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return AuthService(db)
