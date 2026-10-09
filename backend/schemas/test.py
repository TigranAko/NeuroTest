from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TestCreate(BaseModel):
    title: str
    # questions: list[QuestionCreate]


class TestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    author_id: UUID
    title: str
    # questions: list[QuestionResponse]
