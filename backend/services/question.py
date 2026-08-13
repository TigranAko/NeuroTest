from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from schemas.question import QuestionCreate, QuestionResponse
from sqlalchemy.ext.asyncio import AsyncSession


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
        # TODO: verify test_id
        question_id = await self.question.add_one(test_id, question)
        await self._verify_authorship(user_id, question_id)
        await self.db.commit()
        return question_id

    async def get_question(
        self,
        question_id: UUID,
    ) -> QuestionResponse:
        data = await self.question.get_by_id(question_id)
        if data is None:
            raise HTTPException(404, "Question not found")
        question = QuestionResponse.model_validate(data)
        return question

    async def get_questions_test(
        self,
        test_id: UUID,
    ) -> list[QuestionResponse]:
        data = await self.question.get_by_test(test_id)
        if data is None:
            raise HTTPException(404, "Question not found")
        questions: list[QuestionResponse] = []
        for question in data:
            questions.append(QuestionResponse.model_validate(question))
        return questions

    async def delete_question(
        self,
        user_id: UUID,
        question_id: UUID,
    ) -> dict[UUID, list[UUID]]:
        # ) -> QuestionResponse:
        await self._verify_authorship(user_id, question_id)
        question = await self.question.get_by_id(question_id)
        if question is None:
            raise HTTPException(404, "Question not found")
        answers = await self.answer.delete_by_question(question_id)
        await self.question.delete_one(question_id)
        await self.question.shift_positions(question.test_id, question.position)
        await self.db.commit()
        question = {question_id: list(answers)}  # TODO: Change output relust
        return question

    async def _verify_authorship(self, user_id: UUID, question_id: UUID) -> None:
        if user_id != await self.question.get_author_id(question_id):
            raise HTTPException(403)


def get_question_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return QuestionService(db)
