from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.test_output import QuestionOutput
from services.question import QuestionService, get_question_service

router = APIRouter(
    prefix="/api/v1/tests/{test_id}/questions",
    tags=["Question"],
)


@router.post("/")
async def create_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    question: QuestionOutput,
    test_id: UUID,
    question_id: UUID | int | None = None,
) -> UUID:
    return await question_service.add_question(question, test_id, question_id)


@router.get("/")
async def read_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    test_id: UUID,
    question_id: UUID | int = -1,
) -> QuestionOutput:
    return await question_service.get_question(test_id, question_id)


@router.put("/")
async def update_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    question: QuestionOutput,
    test_id: UUID,
    question_id: UUID | int = -1,
) -> UUID:
    return await question_service.update_question(question, test_id, question_id)


@router.delete("/")
async def delete_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    test_id: UUID,
    question_id: UUID | int = -1,
) -> None:
    await question_service.delete_question(test_id, question_id)
