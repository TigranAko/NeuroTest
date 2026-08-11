import json
from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException, UploadFile
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from repositories.test import TestRepository
from schemas.answer import AnswerCreate
from schemas.question import QuestionCreate
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
        author_id: UUID,
        test: TestCreate,
    ) -> UUID:
        test_id = await self.test.add_one(test, author_id)
        await self.db.commit()
        return test_id

    async def import_test(
        self,
        author_id: UUID,
        file: UploadFile,
    ) -> UUID:
        data = await self._get_json(file)
        test = data.copy()
        questions = test.pop("questions")
        tc = TestCreate(**test)
        test_id = await self.test.add_one(tc, author_id)
        for q in questions:
            answers = q.pop("answers")
            qc = QuestionCreate(text=q.get("question"))
            question_id = await self.question.add_one(test_id, qc)
            for a in answers:
                ac = AnswerCreate(**a)
                await self.answer.add_one(question_id, ac)
        await self.db.commit()
        return test_id

    async def _get_json(
        self,
        file: UploadFile,
    ) -> dict:
        content_type = file.content_type
        if content_type != "application/json":
            raise HTTPException(
                422,
                "File Extension does not support",
            )
        data = json.loads(await file.read())
        return data

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
        user_id: UUID,
        test_id: UUID,
    ) -> dict:
        test = await self.get_test(test_id)
        if user_id != test.author_id:
            raise HTTPException(403)
        answers_id = await self.answer.delete_by_test(test_id)
        questions_id = await self.question.delete_by_test(test_id)
        test_id = await self.test.delete_one(test_id)
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
