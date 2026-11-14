import logging
from collections.abc import Sequence
from uuid import UUID

from models.question import Question
from models.test import Test
from repositories.base import BaseRepository
from schemas.question import QuestionCreate, QuestionUpdate
from sqlalchemy import ScalarResult, delete, func, insert, select, update

logger = logging.getLogger(__name__)


class QuestionRepository(BaseRepository[Question, QuestionCreate, QuestionUpdate]):
    model = Question

    async def add_one(
        self,
        test_id: UUID,
        question: QuestionCreate,
    ) -> UUID:
        logger.debug(
            "Create object by id",
            extra={
                "meta": {
                    "test_id": str(test_id),
                    "class": self.__class__.__name__,
                },
            },
        )
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

    async def get_by_test(self, test_id: UUID) -> ScalarResult[Question]:
        logger.debug(
            "Fetch object by test id",
            extra={
                "meta": {
                    "test_id": str(test_id),
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = select(self.model).where(self.model.test_id == test_id)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def get_author_id(self, question_id: UUID) -> UUID | None:
        logger.debug(
            "Fetch author id by question id",
            extra={
                "meta": {
                    "question_id": str(question_id),
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = (
            select(Test.author_id)
            .join(self.model, self.model.test_id == Test.id)
            .where(self.model.id == question_id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalar_one_or_none()

    async def delete_by_test(
        self,
        test_id: UUID,
    ) -> Sequence[UUID]:
        logger.debug(
            "Delete object by test id",
            extra={
                "meta": {
                    "test_id": str(test_id),
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = (
            delete(self.model)
            .where(self.model.test_id == test_id)
            .returning(self.model.id)
        )
        answer = await self.db.execute(stmt)
        return answer.scalars().all()

    async def shift_positions(
        self,
        test_id: UUID,
        from_position: int,
        delta: int = -1,
    ) -> None:
        logger.debug(
            "Shift positions by test id",
            extra={
                "meta": {
                    "test_id": str(test_id),
                    "from_position": from_position,
                    "delta": delta,
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = (
            update(self.model)
            .where(
                self.model.test_id == test_id,
                self.model.position >= from_position,
            )
            .values(position=self.model.position + delta)
        )
        await self.db.execute(stmt)
