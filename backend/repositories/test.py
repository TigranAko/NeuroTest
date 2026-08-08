from uuid import UUID

from models.test import Test
from schemas.test import TestCreate
from sqlalchemy import ScalarResult, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class TestRepository:
    model = Test

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(
        self,
        test: TestCreate,
        author_id: UUID,
    ) -> UUID:
        data = test.model_dump()
        data["author_id"] = author_id
        stmt = insert(self.model).values(**data).returning(self.model.id)
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result

    async def get_by_id(self, test_id: UUID) -> Test | None:
        stmt = select(self.model).where(self.model.id == test_id)
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()

    async def get_tests(self) -> ScalarResult[Test]:
        stmt = select(self.model)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def delete_one(
        self,
        test_id: UUID,
    ) -> UUID | None:
        stmt = (
            delete(self.model).where(self.model.id == test_id).returning(self.model.id)
        )
        test = await self.db.execute(stmt)
        result = test.scalar_one_or_none()
        return result
