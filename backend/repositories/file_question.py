from uuid import UUID

from infrastructure.file_storage import FileStorage
from repositories.interfaces import IQuestionRepository
from schemas.test_output import QuestionOutput


class FileQuestionRepository(IQuestionRepository):
    def __init__(self):
        self.storage = FileStorage()

    async def _number2id(self, number) -> int:
        if number > 0:
            number = number - 1
        elif number == 0:
            number = -1
        return number

    async def add(
        self,
        question: QuestionOutput,
        test_id: UUID,
        question_id: int = 0,
    ) -> UUID:
        async with self.storage.transaction(test_id) as data:
            questions = data.get("questions")
            # TODO: Verify questions
            if question_id == 0:
                questions.append(question)
            elif question_id > 0:
                questions.insert(question, question_id - 1)
            else:
                questions.insert(question, question_id)
        return test_id

    async def get(
        self,
        test_id: UUID,
        question_id: int = 0,
    ) -> QuestionOutput:
        data = await self.storage.read_json(test_id)  # read
        questions = data.get("questions")
        # TODO: Verify questions and question_id
        question_id = self._number2id(question_id)
        question = questions[question_id]
        question_output = QuestionOutput(**question)
        return question_output

    async def update(
        self,
        question: QuestionOutput,
        test_id: UUID,
        question_id: int = 0,
    ) -> UUID:
        async with self.storage.transaction(test_id) as data:
            questions = data.get("questions")
            # TODO: Verify questions and question_id
            question_id = self._number2id(question_id)
            questions[question_id] = question
        return test_id

    async def delete(
        self,
        test_id: UUID,
        question_id: int = 0,
        # question_id_stop: int | None = None,
    ) -> None:
        # TODO: delete many questions
        async with self.storage.transaction(test_id) as data:
            questions = data.get("questions")
            question_id = self._number2id(question_id)
            del questions[question_id]
