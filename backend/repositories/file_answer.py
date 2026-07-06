from uuid import UUID

from infrastructure.file_storage import FileStorage
from repositories.interfaces import IAnswerRepository
from schemas.test_output import AnswerOutput


class FileAnswerRepository(IAnswerRepository):
    def __init__(self):
        self.storage = FileStorage()

    async def _number2id(self, number) -> int:
        if number > 0:
            number = number - 1
        elif number == 0:
            number = -1
        return number

    async def _get_answers(
        self,
        data: dict,
        question_id: int,
        answer_id: int | None = None,
    ) -> list[dict[str, str]]:
        questions = data.get("questions")  # TODO: Verify questions
        question = questions[question_id]  # TODO: Verify questions
        answers = question.get("answers")  # TODO: Verify answers
        return answers

    async def add(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: int = 0,
        answer_id: int = 0,
    ) -> UUID:
        async with self.storage.transaction(test_id) as data:
            answers = self._get_answers(data, question_id)
            question_id = self._number2id(question_id)
            if answer_id == 0:
                answers.append(answer)
            else:
                answer_id = self._number2id(answer_id)
                answers.insert(answer, answer_id)
        return test_id

    async def get(
        self,
        test_id: UUID,
        question_id: int = 0,
        answer_id: int = 0,
    ) -> AnswerOutput:
        question_id = self._number2id(question_id)
        answer_id = self._number2id(answer_id)
        async with self.storage.transaction(test_id, "r") as data:
            answers = self._get_answers(data, question_id)
        answer = answers[answer_id]

        question_output = AnswerOutput(**answer)
        return question_output

    async def update(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: int = 0,
        answer_id: int = 0,
    ) -> UUID:
        question_id = self._number2id(question_id)
        answer_id = self._number2id(answer_id)
        async with self.storage.transaction(test_id) as data:
            answers = self._get_answers(data, question_id)
            answers[answer_id] = answer
        return test_id

    async def delete(
        self,
        test_id: UUID,
        question_id: int = 0,
        answer_id: int = 0,
    ) -> None:
        # TODO: delete many questions
        question_id = self._number2id(question_id)
        answer_id = self._number2id(answer_id)
        async with self.storage.transaction(test_id) as data:
            answers = self._get_answers(data, question_id)
            del answers[answer_id]
