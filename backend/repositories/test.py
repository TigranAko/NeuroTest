from sqlalchemy.orm import selectinload
from uuid import UUID

from models.question import Question
from models.test import Test
from schemas.test import TestCreate
from sqlalchemy import ScalarResult, delete, insert, select, update
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

    async def get_by_author(
        self,
        author_id: UUID,
    ) -> ScalarResult[Test]:
        stmt = select(self.model).where(self.model.author_id == author_id)
        test = await self.db.execute(stmt)
        return test.scalars()

    async def get_tests(self) -> ScalarResult[Test]:
        stmt = select(self.model)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def edit_one(
        self,
        test_id: UUID,
        question: TestCreate,
    ) -> UUID:
        data = question.model_dump()
        stmt = (
            update(self.model)
            .where(self.model.id == test_id)
            .values(data)
            .returning(self.model.id)
        )
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result

    async def delete_one(
        self,
        test_id: UUID,
    ) -> UUID:
        stmt = (
            delete(self.model).where(self.model.id == test_id).returning(self.model.id)
        )
        test = await self.db.execute(stmt)
        result = test.scalar_one()
        return result

    async def export(self, test_id: UUID) -> Test | None:
        stmt = (
            select(self.model)
            .where(self.model.id == test_id)
            .options(selectinload(self.model.questions).selectinload(Question.answers))
        )
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()
