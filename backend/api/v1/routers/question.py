from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.question import QuestionCreate, QuestionResponse
from services.question import QuestionService, get_question_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Question"],
)


@router.post("/tests/{test_id}/questions")
async def create_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    question: QuestionCreate,
    test_id: UUID,
) -> UUID:
    return await question_service.add_question(test_id, question)


@router.get("/questions/{question_id}")
async def read_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    question_id: UUID,
) -> QuestionResponse:
    return await question_service.get_question(question_id)
