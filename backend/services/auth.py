from typing import Annotated
from uuid import UUID, uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from core.settings import auth_settings as settings
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserDB, UserResponse
from services.jwt import jwt_service

fake_db: dict[UUID, UserDB] = {}
ph = PasswordHasher()


class AuthService:
    async def register(
        self,
        user: UserCreate,
    ) -> UserResponse:
        hashed_password = ph.hash(user.password)
        # TODO: Verify user exists
        # TODO: Real DB
        user_data = {
            "user_id": uuid4(),
            "username": user.username,
            "hashed_password": hashed_password,
        }
        user_db = UserDB(**user_data)
        fake_db[user_data["user_id"]] = user_db
        print(fake_db)
        user_response_data = {
            "username": user_db.username,
            "user_id": user_db.user_id,
        }
        user_response = UserResponse(**user_response_data)
        return user_response

    async def login(
        self,
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends],
    ):
        # TODO: Verify user exists
        # TODO: Verify password hash
        # TODO: Real DB
        for user_data in fake_db.values():
            if user_data.username == form_data.username:
                user = user_data
                try:
                    ph.verify(user.hashed_password, form_data.password)
                except VerificationError:
                    raise HTTPException(401, "User Not Found")
                break
        else:
            raise HTTPException(401, "User Not Found")

        access = jwt_service.create_access_token(user.user_id)
        refresh = jwt_service.create_refresh_token(user.user_id)

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.auth_access_expire_minutes * 86400,
        )
        # response.set_cookie(
        #     key="access_token",
        #     value=access,
        #     httponly=True,
        #     secure=True,
        #     samesite="strict",
        #     max_age=settings.auth_refresh_expire_days * 60,
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


def get_auth_service():
    return AuthService()
