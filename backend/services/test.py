import json
import logging
from typing import Annotated
from urllib.parse import quote
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException, UploadFile
from fastapi.responses import Response
from repositories.answer import AnswerRepository
from repositories.question import QuestionRepository
from repositories.test import TestRepository
from schemas.answer import AnswerCreate
from schemas.question import QuestionCreate
from schemas.test import TestCreate, TestResponse
from schemas.test_json import TestJson
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


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
        logger.info(
            "Adding new test",
            extra={
                "meta": {
                    "author_id": str(author_id),
                },
            },
        )
        test_id = await self.test.add_one(test, author_id)
        await self.db.commit()
        logger.info(
            "Test added successfully",
            extra={"meta": {"test_id": str(test_id)}},
        )
        return test_id

    async def import_test(
        self,
        author_id: UUID,
        file: UploadFile,
    ) -> UUID:
        logger.info(
            "Importing test from file",
            extra={"meta": {"author_id": str(author_id), "filename": file.filename}},
        )
        data = await self._get_json(file)
        test = data.copy()
        test["title"] = file.filename
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
        logger.info(
            "Test imported successfully",
            extra={"meta": {"test_id": str(test_id), "filename": file.filename}},
        )
        return test_id

    async def export_test(
        self,
        test_id: UUID,
    ) -> Response:
        logger.info(
            "Exporting test",
            extra={"meta": {"test_id": str(test_id)}},
        )
        test = await self.test.export(test_id)
        if test is None:
            logger.warning(
                "Test not found for export",
                extra={"meta": {"test_id": str(test_id)}},
            )
            raise HTTPException(404, "Test not found")
        body = TestJson.model_validate(test).model_dump_json(indent=4)
        filename = f"{test.title}.json"
        disposition = f"attachment; filename*=UTF-8''{quote(filename)}"
        logger.info(
            "Test exported successfully",
            extra={"meta": {"test_id": str(test_id), "filename": filename}},
        )
        return Response(
            content=body,
            media_type="application/json",
            headers={"Content-Disposition": disposition},
        )

    async def _get_json(
        self,
        file: UploadFile,
    ) -> dict:
        logger.debug(
            "Parsing JSON from uploaded file",
            extra={"meta": {"filename": file.filename}},
        )
        content_type = file.content_type
        if content_type != "application/json":
            logger.warning(
                "Unsupported file content type",
                extra={
                    "meta": {"content_type": content_type, "filename": file.filename}
                },
            )
            raise HTTPException(
                422,
                "File Extension does not support",
            )
        data = json.loads(await file.read())
        logger.debug(
            "JSON from uploaded file parsed successfully",
            extra={"meta": {"filename": file.filename}},
        )
        return data

    async def get_test(
        self,
        test_id: UUID,
    ) -> TestResponse:
        logger.info(
            "Fetching test",
            extra={"meta": {"test_id": str(test_id)}},
        )
        data = await self.test.get_by_id(test_id)
        if data is None:
            logger.warning(
                "Test not found",
                extra={"meta": {"test_id": str(test_id)}},
            )
            raise HTTPException(404, "Test not found")
        logger.info(
            "Test fetched successfully",
            extra={"meta": {"test_id": str(test_id)}},
        )
        return TestResponse.model_validate(data)

    async def get_tests(
        self,
    ) -> list[TestResponse]:
        logger.info("Fetching all tests")
        data = await self.test.get_tests()
        tests: list[TestResponse] = []
        for test in data:
            tests.append(TestResponse.model_validate(test))
        logger.info("All tests fetched successfully")
        return tests

    async def get_author_tests(self, author_id) -> list[TestResponse]:
        logger.info(
            "Fetching tests by author",
            extra={"meta": {"author_id": str(author_id)}},
        )
        data = await self.test.get_by_author(author_id)
        tests: list[TestResponse] = []
        for test in data:
            tests.append(TestResponse.model_validate(test))
        logger.info(
            "Tests fetched by author",
            extra={"meta": {"author_id": str(author_id)}},
        )
        return tests

    async def edit_test(
        self,
        user_id: UUID,
        test_id: UUID,
        test: TestCreate,
    ) -> UUID:
        logger.info(
            "Editing test",
            extra={"meta": {"user_id": str(user_id), "test_id": str(test_id)}},
        )
        test_for_authorship = await self.get_test(test_id)  # TODO need optimize
        if user_id != test_for_authorship.author_id:
            logger.warning(
                "Access denied for editing test",
                extra={"meta": {"user_id": str(user_id), "test_id": str(test_id)}},
            )
            raise HTTPException(403)
        test_id = await self.test.edit_one(test_id, test)
        await self.db.commit()
        logger.info(
            "Test edited successfully",
            extra={"meta": {"user_id": str(user_id), "test_id": str(test_id)}},
        )
        return test_id

    async def delete_test(
        self,
        user_id: UUID,
        test_id: UUID,
    ) -> dict:
        logger.info(
            "Deleting test",
            extra={"meta": {"user_id": str(user_id), "test_id": str(test_id)}},
        )
        test = await self.get_test(test_id)
        if user_id != test.author_id:
            logger.warning(
                "Access denied for deleting test",
                extra={"meta": {"user_id": str(user_id), "test_id": str(test_id)}},
            )
            raise HTTPException(403)
        answers_id = await self.answer.delete_by_test(test_id)
        questions_id = await self.question.delete_by_test(test_id)
        test_id = await self.test.delete_one(test_id)
        await self.db.commit()
        logger.info(
            "Test deleted successfully",
            extra={
                "meta": {
                    "user_id": str(user_id),
                    "test_id": str(test_id),
                    "answers_deleted": len(answers_id),
                    "questions_deleted": len(questions_id),
                }
            },
        )
        return {
            "test_id": test_id,
            "questions_id": list(questions_id),
            "answers_id": list(answers_id),
        }


def get_test_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return TestService(db)
