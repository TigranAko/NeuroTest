from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TestCreate(BaseModel):
    pass
    # questions: list[QuestionCreate]
    # TODO: title


class TestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    author_id: UUID
    # TODO: title
    # questions: list[QuestionResponse]
