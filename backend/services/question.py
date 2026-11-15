import logging
from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class QuestionService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.question = QuestionRepository(db)
        self.answer = AnswerRepository(db)

    async def add_question(
        self,
        user_id: UUID,
        test_id: UUID,
        question: QuestionCreate,
    ) -> UUID:
        logger.info(
            "Adding new question",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "test_id": str(test_id),
                },
            },
        )
        # TODO: verify test_id
        question_id = await self.question.add_one(test_id, question)
        await self._verify_authorship(user_id, question_id)
        await self.db.commit()
        logger.info(
            "Question added successfully",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "test_id": str(test_id),
                    "question_id": str(question_id),
                },
            },
        )
        return question_id

    async def get_question(
        self,
        question_id: UUID,
    ) -> QuestionResponse:
        logger.info(
            "Fetching question",
            extra={
                "meta": {
                    "question_id": str(question_id),
                },
            },
        )
        data = await self.question.get_by_id(question_id)
        if data is None:
            logger.warning(
                "Question not found",
                extra={
                    "meta": {
                        "question_id": str(question_id),
                    },
                },
            )
            raise HTTPException(404, "Question not found")
        question = QuestionResponse.model_validate(data)
        logger.info(
            "Question fetched successfully",
            extra={
                "meta": {
                    "question_id": str(question_id),
                },
            },
        )
        return question

    async def get_questions_test(
        self,
        test_id: UUID,
    ) -> list[QuestionResponse]:
        logger.info(
            "Fetching questions by test id",
            extra={
                "meta": {
                    "test_id": str(test_id),
                },
            },
        )
        data = await self.question.get_by_test(test_id)
        questions: list[QuestionResponse] = []
        for question in data:
            questions.append(QuestionResponse.model_validate(question))
        logger.info(
            "Questions fetched successfully",
            extra={
                "meta": {
                    "test_id": str(test_id),
                },
            },
        )
        return questions

    async def edit_question(
        self,
        user_id: UUID,
        question_id: UUID,
        question: QuestionCreate,
    ) -> UUID:
        logger.info(
            "Editing question",
            extra={"meta": {"user_id": str(user_id), "question_id": str(question_id)}},
        )
        await self._verify_authorship(user_id, question_id)
        question_id = await self.question.edit_one(question_id, question)
        await self.db.commit()
        logger.info(
            "Question edited successfully",
            extra={"meta": {"user_id": str(user_id), "question_id": str(question_id)}},
        )
        return question_id

    async def partial_edit_question(
        self,
        user_id: UUID,
        question_id: UUID,
        question: QuestionUpdate,
    ) -> UUID:
        logger.info(
            "Partial editing question",
            extra={"meta": {"user_id": str(user_id), "question_id": str(question_id)}},
        )
        await self._verify_authorship(user_id, question_id)
        question_id = await self.question.partial_edit_one(question_id, question)
        await self.db.commit()
        logger.info(
            "Question partially edited successfully",
            extra={"meta": {"user_id": str(user_id), "question_id": str(question_id)}},
        )
        return question_id

    async def delete_question(
        self,
        user_id: UUID,
        question_id: UUID,
    ) -> dict[UUID, list[UUID]]:
        logger.info(
            "Deleting question",
            extra={"meta": {"user_id": str(user_id), "question_id": str(question_id)}},
        )
        await self._verify_authorship(user_id, question_id)
        question = await self.question.get_by_id(question_id)
        if question is None:
            logger.warning(
                "Question not found",
                extra={
                    "meta": {
                        "question_id": str(question_id),
                        "user_id": str(user_id),
                    },
                },
            )
            raise HTTPException(404, "Question not found")
        answers = await self.answer.delete_by_question(question_id)
        await self.question.delete_one(question_id)
        await self.question.shift_positions(question.test_id, question.position)
        await self.db.commit()
        question = {question_id: list(answers)}  # TODO: Change output relust
        logger.info(
            "Question deleted successfully",
            extra={"meta": {"user_id": str(user_id), "question_id": str(question_id)}},
        )
        return question

    async def _verify_authorship(self, user_id: UUID, question_id: UUID) -> None:
        if user_id != await self.question.get_author_id(question_id):
            logger.warning(
                "Authorship verification failed",
                extra={
                    "meta": {
                        "question_id": str(question_id),
                        "user_id": str(user_id),
                    },
                },
            )
            raise HTTPException(403)


def get_question_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return QuestionService(db)
