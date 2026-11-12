from uuid import UUID

from models.question import Question
from models.test import Test
from repositories.base import BaseRepository
from schemas.test import TestCreate, TestUpdate
from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.orm import selectinload


class TestRepository(BaseRepository[Test, TestCreate, TestUpdate]):
    model = Test

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

    async def export(self, test_id: UUID) -> Test | None:
        stmt = (
            select(self.model)
            .where(self.model.id == test_id)
            .options(selectinload(self.model.questions).selectinload(Question.answers))
        )
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()
