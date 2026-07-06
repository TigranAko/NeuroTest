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
        async with self.storage.transaction(test_id, "w") as data:
            data.update(test)  # Мутация data
        return test_id

    async def get(
        self,
        test_id: UUID,
    ) -> TestOutput:
        async with self.storage.transaction(test_id, "r") as data:
            return data

    async def get_all(
        self,
    ) -> list[str]:
        return await self.storage.get_files()

    async def update(
        self,
        test: TestOutput,
        test_id: UUID,
    ) -> UUID:
        async with self.storage.transaction(test_id, "w") as data:
            data.update(test)  # Мутация data
        return test_id

    async def delete(
        self,
        test_id: UUID,
    ) -> None:
        await self.storage.delete_json(test_id)
