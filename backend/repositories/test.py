import logging
from uuid import UUID

from models.question import Question
from models.test import Test
from repositories.base import BaseRepository
from schemas.test import TestCreate, TestUpdate
from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)


class TestRepository(BaseRepository[Test, TestCreate, TestUpdate]):
    model = Test

    async def add_one(
        self,
        test: TestCreate,
        author_id: UUID,
    ) -> UUID:
        data = test.model_dump()
        data["author_id"] = author_id
        stmt = insert(self.model).values(**data).returning(self.model.id)
        test_id = await self.db.execute(stmt)
        result = test_id.scalar_one()
        logger.debug(
            "Create object by id",
            extra={
                "meta": {
                    "author_id": str(author_id),
                    "test_id": str(result),
                    "class": self.__class__.__name__,
                },
            },
        )
        return result

    async def get_by_author(
        self,
        author_id: UUID,
    ) -> ScalarResult[Test]:
        logger.debug(
            "Fetch objects by author id",
            extra={
                "meta": {
                    "author_id": str(author_id),
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = select(self.model).where(self.model.author_id == author_id)
        test = await self.db.execute(stmt)
        return test.scalars()

    async def get_tests(self) -> ScalarResult[Test]:
        logger.debug(
            "Fetch objects",
            extra={
                "meta": {
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = select(self.model)
        answer = await self.db.execute(stmt)
        return answer.scalars()

    async def export(
        self,
        test_id: UUID,
    ) -> Test | None:
        logger.debug(
            "Export object",
            extra={
                "meta": {
                    "test_id": str(test_id),
                    "class": self.__class__.__name__,
                },
            },
        )
        stmt = (
            select(self.model)
            .where(self.model.id == test_id)
            .options(selectinload(self.model.questions).selectinload(Question.answers))
        )
        test = await self.db.execute(stmt)
        return test.scalar_one_or_none()
