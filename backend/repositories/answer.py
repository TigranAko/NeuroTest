from uuid import UUID

from models.answer import Answer
from schemas.answer import AnswerCreate
from sqlalchemy import ScalarResult, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class AnswerRepository:
    model = Answer

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_one(
        self,
        question_id: UUID,
        answer: AnswerCreate,
    ) -> UUID:
        data = answer.model_dump()
        data["question_id"] = question_id
        stmt = insert(self.model).values(**data).returning(self.model.id)
        answer_id = await self.db.execute(stmt)
        result = answer_id.scalar_one()
        return result

    async def get_by_id(self, answer_id: UUID) -> Answer | None:
        stmt = select(self.model).where(self.model.id == answer_id)
        answer = await self.db.execute(stmt)
        return answer.scalar_one_or_none()

    async def get_by_question(self, question_id: UUID) -> ScalarResult[Answer]:
        stmt = select(self.model).where(self.model.question_id == question_id)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def delete_one(self, answer_id: UUID) -> UUID | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == answer_id)
            .returning(self.model.id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalar_one_or_none()
