from abc import ABC, abstractmethod
from uuid import UUID

from schemas.test_output import TestOutput, QuestionOutput, AnswerOutput


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


class IQuestionRepository(ABC):
    @abstractmethod
    async def add(
        self,
        test_id: UUID,
        question: QuestionOutput,
        question_id: UUID | int | None = None,
    ) -> UUID:
        pass

    @abstractmethod
    async def get(
        self,
        test_id: UUID,
        question_id: UUID | int,
    ) -> QuestionOutput:
        pass

    @abstractmethod
    async def update(
        self,
        test_id: UUID,
        question_id: UUID | int,
        question: QuestionOutput,
    ) -> UUID:
        pass

    @abstractmethod
    async def delete(
        self,
        test_id: UUID,
        question_id: UUID | int,
    ) -> None:
        pass


class IAnswerRepository(ABC):
    @abstractmethod
    async def add(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> UUID:
        pass

    @abstractmethod
    async def get(
        self,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> AnswerOutput:
        pass

    @abstractmethod
    async def update(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> UUID:
        pass

    @abstractmethod
    async def delete(
        self,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> None:
        pass
