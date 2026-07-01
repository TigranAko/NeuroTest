from abc import ABC, abstractmethod
from uuid import UUID

from schemas.test_output import TestOutput


class ITestRepository(ABC):
    @abstractmethod
    async def add(self, test: TestOutput) -> UUID:
        pass

    @abstractmethod
    async def get(self, test_id: UUID) -> TestOutput:
        pass

    @abstractmethod
    async def get_all(self) -> list[str]:
        pass

    @abstractmethod
    async def update(self, test_id: UUID, test: TestOutput) -> UUID:
        pass

    @abstractmethod
    async def delete(self, test_id: UUID) -> None:
        pass
