from pydantic import BaseModel


class AnswerOutput(BaseModel):
    text: str
    isCorrect: bool


class QuestionOutput(BaseModel):
    question: str
    answers: list[AnswerOutput]


class TestOutput(BaseModel):
    questions: list[QuestionOutput]
