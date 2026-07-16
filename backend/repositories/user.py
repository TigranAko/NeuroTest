from uuid import UUID

from models.user import User
from schemas.user import UserCreate
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    model = User

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(self, user: UserCreate) -> UUID:
        stmt = insert(self.model).values(**user.model_dump()).returning(self.model.id)
        # TODO: add pagination and filtration
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result
