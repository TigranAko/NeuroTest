from uuid import UUID

from repositories.file_question import FileQuestionRepository
from repositories.interfaces import IQuestionRepository
from schemas.test_output import QuestionOutput


class QuestionService:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    async def add_question(
        self,
        test_id: UUID,
        question: QuestionOutput,
        question_id: int | UUID | None = None,
    ) -> UUID:
        # if question_id is none append else insert by question_id
        test_id = await self.repo.add(test_id, question)
        return test_id

    async def get_question(
        self,
        test_id: UUID,
        question_id: int | UUID = -1,
    ) -> QuestionOutput:
        return await self.repo.get(test_id, question_id)

    async def update_question(
        self,
        test_id: UUID,
        question: QuestionOutput,
        question_id: int | UUID = -1,
    ) -> UUID:
        return await self.repo.update(test_id, question, question_id)

    async def delete_question(
        self,
        test_id: UUID,
        question_id: int | UUID = -1,
    ) -> None:
        return await self.repo.delete(test_id, question_id)


def get_question_service():
    return QuestionService(FileQuestionRepository())
