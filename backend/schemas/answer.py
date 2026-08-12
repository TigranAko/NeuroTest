from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnswerCreate(BaseModel):
    text: str
    isCorrect: bool
    # TODO:
    # position: int


class AnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    position: int
    text: str
    isCorrect: bool
    # TODO:
    # answers: list["Answer"]
