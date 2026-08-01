from uuid import UUID

from models.question import Question
from schemas.question import QuestionCreate
from sqlalchemy import insert, select
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
        data["test_id"] = test_id
        stmt = insert(self.model).values(**data).returning(self.model.id)
        user_id = await self.db.execute(stmt)
        result = user_id.scalar_one()
        return result

    async def get_by_id(self, question_id: UUID) -> Question | None:
        stmt = select(self.model).where(self.model.id == question_id)
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()
