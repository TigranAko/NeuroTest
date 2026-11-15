import logging
from uuid import UUID

from models.user import User
from schemas.user import UserCreate
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class UserRepository:
    model = User

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(self, user: UserCreate) -> UUID:
        logger.debug(
            "Create user",
            extra={
                "meta": {
                    "username": user.username,
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = insert(self.model).values(**user.model_dump()).returning(self.model.id)
        # TODO: add pagination and filtration
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result

    async def get_by_username(self, username: str) -> User | None:
        logger.debug(
            "Get user by username",
            extra={
                "meta": {
                    "username": username,
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = select(self.model).where(self.model.username == username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        logger.debug(
            "Get user by id",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = select(self.model).where(self.model.id == user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()
