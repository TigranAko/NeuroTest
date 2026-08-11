from uuid import UUID

from pydantic import BaseModel


class AnswerOutput(BaseModel):
    text: str
    isCorrect: bool


class QuestionOutput(BaseModel):
    question: str
    answers: list[AnswerOutput]


class TestOutput(BaseModel):
    author_id: UUID
    questions: list[QuestionOutput]
