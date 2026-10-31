import logging
from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.answer import AnswerRepository
from schemas.answer import AnswerCreate, AnswerResponse, AnswerUpdate
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AnswerService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = AnswerRepository(db)

    async def add_answer(
        self,
        user_id: UUID,
        answer: AnswerCreate,
        question_id: UUID,
    ) -> UUID:
        logger.info(
            "Adding new answer",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "question_id": str(question_id),
                },
            },
        )
        answer_id = await self.repo.add_one(question_id, answer)
        await self._verify_authorship(user_id, answer_id)
        await self.db.commit()
        logger.info(
            "New answer added successfully",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "question_id": str(question_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        return answer_id

    async def get_answer(
        self,
        answer_id: UUID,
    ) -> AnswerResponse:
        logger.info(
            "Fetching answer",
            extra={
                "meta": {
                    "answer_id": str(answer_id),
                },
            },
        )
        data = await self.repo.get_by_id(answer_id)
        if data is None:
            logger.warning(
                "Answer not found",
                extra={
                    "meta": {
                        "answer_id": str(answer_id),
                    },
                },
            )
            raise HTTPException(404, "Answer not found")
        answer = AnswerResponse.model_validate(data)
        logger.info(
            "Answer fetched successfully",
            extra={
                "meta": {
                    "answer_id": str(answer_id),
                },
            },
        )
        return answer

    async def get_answers_question(
        self,
        question_id: UUID,
    ) -> list[AnswerResponse]:
        logger.info(
            "Fetching answers by question id",
            extra={
                "meta": {
                    "question_id": str(question_id),
                },
            },
        )
        data = await self.repo.get_by_question(question_id)
        answers: list[AnswerResponse] = []
        for answer in data:
            answers.append(AnswerResponse.model_validate(answer))
        logger.info(
            "Answers fetched by question id successfully",
            extra={
                "meta": {
                    "question_id": str(question_id),
                    "count": len(answers),
                },
            },
        )
        return answers

    async def edit_answer(
        self,
        user_id: UUID,
        answer: AnswerCreate,
        answer_id: UUID,
    ) -> UUID:
        logger.info(
            "Editing answer",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        await self._verify_authorship(user_id, answer_id)
        answer_id = await self.repo.edit_one(answer_id, answer)
        await self.db.commit()
        logger.info(
            "Answer edited successfully",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        return answer_id

    async def partial_edit_answer(
        self,
        user_id: UUID,
        answer: AnswerUpdate,
        answer_id: UUID,
    ) -> UUID:
        logger.info(
            "Partial editing answer",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        await self._verify_authorship(user_id, answer_id)
        answer_id = await self.repo.partial_edit_one(answer_id, answer)
        await self.db.commit()
        logger.info(
            "Answer partially edited successfully",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        return answer_id

    async def delete_answer(
        self,
        user_id: UUID,
        answer_id: UUID,
    ) -> UUID:
        logger.info(
            "Deleting answer",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        await self._verify_authorship(user_id, answer_id)
        answer = await self.repo.get_by_id(answer_id)
        if answer is None:
            logger.warning(
                "Answer not found",
                extra={
                    "meta": {
                        "answer_id": str(answer_id),
                    },
                },
            )
            raise HTTPException(404, "Answer not found")
        await self.repo.delete_one(answer_id)
        await self.repo.shift_positions(answer.question_id, answer.position)
        await self.db.commit()
        logger.info(
            "Answer deleted successfully",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "answer_id": str(answer_id),
                },
            },
        )
        return answer_id

    async def _verify_authorship(self, user_id: UUID, answer_id: UUID) -> None:
        if user_id != await self.repo.get_author_id(answer_id):
            logger.warning(
                "Authorship verification failed",
                extra={
                    "meta": {
                        "answer_id": str(answer_id),
                        "user_id": str(user_id),
                    },
                },
            )
            raise HTTPException(403)


def get_answer_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return AnswerService(db)
