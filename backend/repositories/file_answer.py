from uuid import UUID


from infrastructure.file_storage import FileStorage
from repositories.interfaces import IAnswerRepository
from schemas.test_output import AnswerOutput, TestOutput


class FileAnswerRepository(IAnswerRepository):
    def __init__(self):
        self.storage = FileStorage()

    async def add(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int | None = None,
    ) -> UUID:
        data = await self.storage.read_json(test_id)

        questions = data.get("questions")
        # TODO: Verify questions, answers
        question = questions[question_id]
        answers = question.get("answers")

        if answer_id is None:
            answers.append(answer)
        else:
            answers.insert(answer, answer_id)

        test = TestOutput(**data)
        await self.storage.create_json(test_id, test)
        return test_id

    async def get(
        self,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> AnswerOutput:
        data = await self.storage.read_json(test_id)  # read
        questions = data.get("questions")
        # TODO: Verify questions and question_id, answer_id

        question = questions[question_id]
        answers = question["answers"]
        answer = answers[answer_id]

        question_output = AnswerOutput(**answer)
        return question_output

    async def update(
        self,
        answer: AnswerOutput,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> UUID:
        data = await self.storage.read_json(test_id)
        questions = data.get("questions")
        # TODO: Verify questions and question_id

        question = questions[question_id]
        answers = question["answers"]
        answers[answer_id] = answer

        test = TestOutput(**data)
        await self.storage.create_json(test_id, test)
        return test_id

    async def delete(
        self,
        test_id: UUID,
        question_id: UUID | int,
        answer_id: int,
    ) -> None:
        # TODO: delete many questions
        data = await self.storage.read_json(test_id)
        questions = data.get("questions")
        question = questions[question_id]
        answers = question["answers"]
        del answers[answer_id]
        test = TestOutput(**data)
        await self.storage.create_json(test_id, test)
