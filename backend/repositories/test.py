from uuid import UUID

from models.test import Test
from schemas.test import TestCreate
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class TestRepository:
    model = Test

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(
        self,
        test: TestCreate,
    ) -> UUID:
        stmt = insert(self.model).values(**test.model_dump()).returning(self.model.id)
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result

    async def get_by_id(self, test_id: UUID) -> Test | None:
        stmt = select(self.model).where(self.model.id == test_id)
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()
