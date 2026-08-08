from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AnswerCreate(BaseModel):
    text: str
    isCorrect: bool
    # TODO:
    # position: int


class AnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    isCorrect: bool
    id: UUID
    # TODO:
    # position: int
    # answers: list["Answer"]
