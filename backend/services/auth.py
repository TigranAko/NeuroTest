from uuid import UUID, uuid4

from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserDB, UserResponse
from services.jwt import jwt_service
from core.settings import auth_settings as settings

fake_db: dict[UUID, UserDB] = dict()


class AuthService:
    async def register(
        self,
        user: UserCreate,
    ) -> UserResponse:
        hashed_password = user.password  # TODO: Hash
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
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        # TODO: Verify user exists
        # TODO: Verify password hash
        # TODO: Real DB
        for user_id, user_data in fake_db.items():
            if user_data.username == form_data.username:
                user = user_data
                break
        else:
            print("Пользователь не найден")

        access = jwt_service.create_access_token(user.id)
        refresh = jwt_service.create_refresh_token(user.id)

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.auth_access_expire_minutes * 86400,
        )
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.auth_refresh_expire_days * 60,
        )
        # return {"access_token": access, "token_type": "Bearer"}
        return UserResponse(
            **{
                "username": user.username,
                "user_id": user.user_id,
            }
        )


def get_auth_service():
    return AuthService()
