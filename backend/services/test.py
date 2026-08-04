from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from repositories.test import TestRepository
from schemas.test import TestCreate, TestResponse
from sqlalchemy.ext.asyncio import AsyncSession


class TestService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.test = TestRepository(db)
        self.question = QuestionRepository(db)
        self.answer = AnswerRepository(db)

    async def add_test(
        self,
        test: TestCreate,
    ) -> UUID:
        test_id = await self.test.add_one(test)
        await self.db.commit()
        return test_id

    async def get_test(
        self,
        test_id: UUID,
    ) -> TestResponse:
        data = await self.test.get_by_id(test_id)
        if data is None:
            raise HTTPException(404, "Test not found")
        return TestResponse.model_validate(data)

    async def get_tests(
        self,
    ) -> list[TestResponse]:
        data = await self.test.get_tests()
        if data is None:
            raise HTTPException(404, "Test not found")
        tests: list[TestResponse] = []
        for test in data:
            tests.append(TestResponse.model_validate(test))
        return tests

    async def delete_test(
        self,
        test_id: UUID,
    ) -> dict:
        answers_id = await self.answer.delete_by_test(test_id)
        questions_id = await self.question.delete_by_test(test_id)
        test_id: UUID | None = await self.test.delete_one(test_id)
        if test_id is None:
            raise HTTPException(404, "Test not found")
        await self.db.commit()
        return {
            "test_id": test_id,
            "questions_id": list(questions_id),
            "answers_id": list(answers_id),
        }


def get_test_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return TestService(db)
