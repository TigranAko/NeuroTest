from uuid import UUID

from repositories.file_question import FileQuestionRepository
from repositories.interfaces import IQuestionRepository
from schemas.test_output import QuestionOutput


class QuestionService:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    async def add_question(
        self,
        question: QuestionOutput,
        test_id: UUID,
        question_id: int | UUID,
    ) -> UUID:
        # if question_id is none append else insert by question_id
        test_id = await self.repo.add(question, test_id)
        return test_id

    async def get_question(
        self,
        test_id: UUID,
        question_id: int | UUID,
    ) -> QuestionOutput:
        return await self.repo.get(test_id, question_id)

    async def update_question(
        self,
        question: QuestionOutput,
        test_id: UUID,
        question_id: int | UUID,
    ) -> UUID:
        return await self.repo.update(question, test_id, question_id)

    async def delete_question(
        self,
        test_id: UUID,
        question_id: int | UUID,
    ) -> None:
        return await self.repo.delete(test_id, question_id)


def get_question_service():
    return QuestionService(FileQuestionRepository())
