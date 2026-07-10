from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import UUID

import jwt
from core.settings import auth_settings as settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWTError


class JWTService:
    def __init__(
        self,
        secret: str,
        algorithm: str,
    ):
        self.secret = secret
        self.algorithm = algorithm

    def _create_token(
        self,
        user_id: UUID,
        expires_delta: timedelta,
        token_type: Literal["access", "refresh"],
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + expires_delta,
            "type": token_type,  # "access" или "refresh"
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        return self._create_token(
            user_id,
            timedelta(minutes=settings.auth_access_expire_minutes),
            "access",
        )

    def create_refresh_token(
        self,
        user_id: UUID,
    ) -> str:
        return self._create_token(
            user_id,
            timedelta(days=settings.auth_refresh_expire_days),
            "refresh",
        )

    def decode_token(
        self,
        token: str,
    ) -> None | dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"require": ["exp", "iat", "sub", "type"]},
            )
        except PyJWTError:
            return None

    def verify_token(
        self,
        token: str,
        allowed_types: list[str],
    ) -> None | UUID:
        payload = self.decode_token(token)
        if not payload:
            return None
        if payload.get("type") not in allowed_types:
            return None
        try:
            return UUID(payload["sub"])
        except (KeyError, ValueError):
            return None


jwt_service = JWTService(settings.auth_jwt_secret, settings.auth_algorithm)
security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UUID:
    if not credentials:
        raise HTTPException(
            401, detail="Missing token", headers={"WWW-Authenticate": "Bearer"}
        )
    user_id = jwt_service.verify_token(
        credentials.credentials, allowed_types=["access"]
    )
    if user_id is None:
        raise HTTPException(
            401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
