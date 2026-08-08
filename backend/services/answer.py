from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.answer import AnswerRepository
from schemas.answer import AnswerCreate, AnswerResponse
from sqlalchemy.ext.asyncio import AsyncSession


class AnswerService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = AnswerRepository(db)

    async def add_answer(
        self,
        answer: AnswerCreate,
        question_id: UUID,
    ) -> UUID:
        answer_id = await self.repo.add_one(question_id, answer)
        await self.db.commit()
        return answer_id

    async def get_answer(
        self,
        answer_id: UUID,
    ) -> AnswerResponse:
        data = await self.repo.get_by_id(answer_id)
        if data is None:
            raise HTTPException(404, "Answer not found")
        answer = AnswerResponse.model_validate(data)
        return answer

    async def get_answers_question(
        self,
        question_id: UUID,
    ) -> list[AnswerResponse]:
        data = await self.repo.get_by_question(question_id)
        if data is None:
            raise HTTPException(404, "Answer not found")
        answers: list[AnswerResponse] = []
        for answer in data:
            answers.append(AnswerResponse.model_validate(answer))
        return answers

    async def delete_answer(
        self,
        answer_id: UUID,
    ) -> UUID:
        answer = await self.repo.delete_one(answer_id)
        if answer is None:
            raise HTTPException(404, "Answer not found")
        await self.db.commit()
        return answer


def get_answer_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return AnswerService(db)
