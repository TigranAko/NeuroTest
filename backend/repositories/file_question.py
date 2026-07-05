from uuid import UUID


from infrastructure.file_storage import FileStorage
from repositories.interfaces import IQuestionRepository
from schemas.test_output import QuestionOutput


class FileQuestionRepository(IQuestionRepository):
    def __init__(self):
        self.storage = FileStorage()

    async def add(
        self,
        test_id: UUID,
        question: QuestionOutput,
        question_id: int | None = None,
    ) -> UUID:
        async with self.storage.transaction(test_id) as data:
            questions = data.get("questions")
            # TODO: Verify questions
            if question_id is None:
                questions.append(question)
            else:
                questions.insert(question, question_id)
        return test_id

    async def get(
        self,
        test_id: UUID,
        question_id: int = -1,
    ) -> QuestionOutput:
        data = await self.storage.read_json(test_id)  # read
        questions = data.get("questions")
        # TODO: Verify questions and question_id

        question = questions[question_id]

        question_output = QuestionOutput(**question)
        return question_output

    async def update(
        self,
        test_id: UUID,
        question: QuestionOutput,
        question_id: int = -1,
    ) -> UUID:
        async with self.storage.transaction(test_id) as data:
            questions = data.get("questions")
            # TODO: Verify questions and question_id
            questions[question_id] = question
        return test_id

    async def delete(
        self,
        test_id: UUID,
        question_id: int,
        # question_id_stop: int | None = None,
    ) -> None:
        # TODO: delete many questions
        async with self.storage.transaction(test_id) as data:
            questions = data.get("questions")
            del questions[question_id]
