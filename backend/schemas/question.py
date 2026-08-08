from uuid import UUID

from pydantic import BaseModel, ConfigDict


class QuestionCreate(BaseModel):
    text: str
    # TODO:
    # answers: list["Answer"]
    # position: int


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    id: UUID
    # TODO:
    # position: int
    # answers: list["Answer"]
