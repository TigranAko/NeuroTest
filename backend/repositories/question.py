from collections.abc import Sequence
from uuid import UUID

from models.question import Question
from models.test import Test
from schemas.question import QuestionCreate
from sqlalchemy import ScalarResult, delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionRepository:
    model = Question

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(
        self,
        test_id: UUID,
        question: QuestionCreate,
    ) -> UUID:
        data = question.model_dump()
        position_subq = (
            select(func.count()).where(self.model.test_id == test_id).scalar_subquery()
        )
        stmt = (
            insert(self.model)
            .values(test_id=test_id, **data, position=position_subq)
            .returning(self.model.id)
        )
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result

    async def get_by_id(self, question_id: UUID) -> Question | None:
        stmt = select(self.model).where(self.model.id == question_id)
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()

    async def get_by_test(self, test_id: UUID) -> ScalarResult[Question]:
        stmt = select(self.model).where(self.model.test_id == test_id)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def get_author_id(self, question_id: UUID) -> UUID | None:
        stmt = (
            select(Test.author_id)
            .join(self.model, self.model.test_id == Test.id)
            .where(self.model.id == question_id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalar_one_or_none()

    async def delete_one(
        self,
        question_id: UUID,
    ) -> UUID | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == question_id)
            .returning(self.model.id)
        )
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one_or_none()
        return result

    async def delete_by_test(
        self,
        test_id: UUID,
    ) -> Sequence[UUID]:
        stmt = (
            delete(self.model)
            .where(self.model.test_id == test_id)
            .returning(self.model.id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalars().all()
