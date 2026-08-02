from typing import Annotated
from uuid import UUID

from core.database import get_db
from fastapi import Depends, HTTPException
from repositories.test import TestRepository
from schemas.test import TestCreate, TestResponse
from sqlalchemy.ext.asyncio import AsyncSession


class TestService:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = TestRepository(db)

    async def add_test(
        self,
        test: TestCreate,
    ) -> UUID:
        test_id = await self.repo.add_one(test)
        await self.db.commit()
        return test_id

    async def get_test(
        self,
        test_id: UUID,
    ) -> TestResponse:
        data = await self.repo.get_by_id(test_id)
        if data is None:
            raise HTTPException(404, "Test not found")
        return TestResponse.model_validate(data)

    async def get_tests(
        self,
    ) -> list[TestResponse]:
        data = await self.repo.get_tests()
        if data is None:
            raise HTTPException(404, "Test not found")
        tests: list[TestResponse] = []
        for test in data:
            tests.append(TestResponse.model_validate(test))
        return tests


def get_test_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return TestService(db)
