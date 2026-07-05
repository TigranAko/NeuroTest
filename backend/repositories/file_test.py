from uuid import UUID, uuid4

from infrastructure.file_storage import FileStorage
from repositories.interfaces import ITestRepository
from schemas.test_output import TestOutput


class FileTestRepository(ITestRepository):
    def __init__(self):
        self.storage = FileStorage()

    async def add(
        self,
        test: TestOutput,
    ) -> UUID:
        test_id = uuid4()
        await self.storage.create_json(test, test_id)
        return test_id

    async def get(
        self,
        test_id: UUID,
    ) -> TestOutput:
        data = await self.storage.read_json(test_id)  # read
        test_output = TestOutput(**data)
        return test_output

    async def get_all(
        self,
    ) -> list[str]:
        return await self.storage.get_files()

    async def update(
        self,
        test: TestOutput,
        test_id: UUID,
    ) -> UUID:
        file_data = await self.storage.create_json(test, test_id)
        return file_data["file"]

    async def delete(
        self,
        test_id: UUID,
    ) -> None:
        await self.storage.delete_json(test_id)
