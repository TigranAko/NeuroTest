from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.question import QuestionRepository
from schemas.question import QuestionCreate, QuestionResponse
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = QuestionRepository(db)

    async def add_question(
        self,
        test_id: UUID,
        question: QuestionCreate,
    ) -> UUID:
        test_id = await self.repo.add_one(test_id, question)
        await self.db.commit()
        return test_id

    async def get_question(
        self,
        question_id: UUID,
    ) -> QuestionResponse:
        data = await self.repo.get_by_id(question_id)
        if data is None:
            raise HTTPException(404, "Question not found")
        question = QuestionResponse.model_validate(data)
        return question

    async def get_questions_test(
        self,
        test_id: UUID,
    ) -> list[QuestionResponse]:
        data = await self.repo.get_by_test(test_id)
        if data is None:
            raise HTTPException(404, "Question not found")
        questions: list[QuestionResponse] = []
        for question in data:
            questions.append(QuestionResponse.model_validate(question))
        return questions


def get_question_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return QuestionService(db)
