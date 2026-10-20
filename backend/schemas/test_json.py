from pydantic import BaseModel, ConfigDict, Field


class AnswerJson(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    isCorrect: bool


class QuestionJson(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    question: str = Field(validation_alias="text")
    answers: list[AnswerJson]


class TestJson(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    questions: list[QuestionJson]
