import json
from uuid import UUID

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from repositories.file_test import FileTestRepository
from repositories.interfaces import ITestRepository
from schemas.test_output import TestOutput


class TestService:
    def __init__(self, repo: ITestRepository):
        self.repo = repo

    async def _read_test_from_file(
        self,
        test_file: UploadFile,
    ) -> TestOutput:
        file_type = test_file.content_type
        if file_type != "application/json":
            raise HTTPException(422)
        file_content = await test_file.read()
        file_text = file_content.decode("utf-8")
        data = json.loads(file_text)
        try:
            test = TestOutput(**data)
        except ValidationError:
            raise HTTPException(422)
        return test

    async def add_test_from_file(
        self,
        test_file: UploadFile,
    ) -> UUID:
        test = await self._read_test_from_file(test_file)
        return await self.add_test(test)

    async def add_test(
        self,
        test: TestOutput,
    ) -> UUID:
        test_id = await self.repo.add(test)
        return test_id

    async def get_test(
        self,
        test_id: UUID,
    ) -> TestOutput:
        return await self.repo.get(test_id)

    async def get_tests(
        self,
    ) -> list[str]:
        # TODO: Нужно поменять структуру, добавить метаданные, сейчас возвращается list[UUID], нужно list[dict]
        return await self.repo.get_all()

    async def update_test_from_file(
        self,
        test_file: UploadFile,
        test_id: UUID,
    ) -> UUID:
        test = await self._read_test_from_file(test_file)
        return await self.update_test(test, test_id)

    async def update_test(
        self,
        test: TestOutput,
        test_id: UUID,
    ) -> UUID:
        return await self.repo.update(test, test_id)

    async def delete_test(
        self,
        test_id: UUID,
    ) -> None:
        return await self.repo.delete(test_id)


def get_test_service():
    return TestService(FileTestRepository())
