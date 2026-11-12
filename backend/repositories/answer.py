from collections.abc import Sequence
from uuid import UUID

from models.answer import Answer
from models.question import Question
from models.test import Test
from repositories.base import BaseRepository
from schemas.answer import AnswerCreate, AnswerUpdate
from sqlalchemy import ScalarResult, delete, func, insert, select, update


class AnswerRepository(BaseRepository[Answer, AnswerCreate, AnswerUpdate]):
    model = Answer

    async def add_one(
        self,
        question_id: UUID,
        answer: AnswerCreate,
    ) -> UUID:
        position_subq = (
            select(func.count())
            .where(self.model.question_id == question_id)
            .scalar_subquery()
        )
        stmt = (
            insert(self.model)
            .values(
                text=answer.text,
                isCorrect=answer.isCorrect,
                question_id=question_id,
                position=position_subq,
            )
            .returning(self.model.id)
        )
        answer_id = await self.db.execute(stmt)
        result = answer_id.scalar_one()
        return result

    async def get_by_question(self, question_id: UUID) -> ScalarResult[Answer]:
        stmt = select(self.model).where(self.model.question_id == question_id)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def get_author_id(self, answer_id: UUID) -> UUID | None:
        stmt = (
            select(Test.author_id)
            .join(Question, Question.test_id == Test.id)
            .join(self.model, self.model.question_id == Question.id)
            .where(self.model.id == answer_id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalar_one_or_none()

    async def delete_by_question(
        self,
        question_id: UUID,
    ) -> Sequence[UUID]:
        stmt = (
            delete(self.model)
            .where(self.model.question_id == question_id)
            .returning(self.model.id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalars().all()

    async def delete_by_test(
        self,
        test_id: UUID,
    ) -> Sequence[UUID]:
        parent = Question
        stmt = (
            delete(self.model)
            .where(
                self.model.question_id.in_(
                    select(parent.id).where(parent.test_id == test_id)
                )
            )
            .returning(self.model.id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalars().all()

    async def shift_positions(
        self,
        question_id: UUID,
        from_position: int,
        delta: int = -1,
    ) -> None:
        stmt = (
            update(self.model)
            .where(
                self.model.question_id == question_id,
                self.model.position >= from_position,
            )
            .values(position=self.model.position + delta)
        )
        await self.db.execute(stmt)
