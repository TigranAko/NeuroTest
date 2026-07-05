from uuid import UUID

from repositories.file_answer import FileAnswerRepository
from repositories.interfaces import IAnswerRepository
from schemas.test_output import AnswerOutput


class AnswerService:
    def __init__(self, repo: IAnswerRepository):
        self.repo = repo

    async def add_answer(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: int | UUID | None = None,
        answer_id: int | None = None,
    ) -> UUID:
        # if question_id is none append else insert by question_id
        test_id = await self.repo.add(answer, test_id, question_id, answer_id)
        return test_id

    async def get_answer(
        self,
        test_id: UUID,
        question_id: int | UUID | None = None,
        answer_id: int = -1,
    ) -> AnswerOutput:
        return await self.repo.get(test_id, question_id, answer_id)

    async def update_answer(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: UUID | int = -1,
        answer_id: int = -1,
    ) -> UUID:
        return await self.repo.update(answer, test_id, question_id, answer_id)

    async def delete_answer(
        self,
        test_id: UUID,
        question_id: int | UUID = -1,
        answer_id: int | UUID = -1,
    ) -> None:
        return await self.repo.delete(test_id, question_id, answer_id)


def get_answer_service():
    return AnswerService(FileAnswerRepository())
