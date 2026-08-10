from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.question import QuestionCreate, QuestionResponse
from services.jwt import get_current_user_id
from services.question import QuestionService, get_question_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Question"],
)


@router.post("/tests/{test_id}/questions")
async def create_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    question: QuestionCreate,
    test_id: UUID,
) -> UUID:
    return await question_service.add_question(user_id, test_id, question)


@router.get("/tests/{test_id}/questions")
async def get_questions_test(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    test_id: UUID,
) -> list[QuestionResponse]:
    return await question_service.get_questions_test(test_id)


@router.get("/questions/{question_id}")
async def read_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    question_id: UUID,
) -> QuestionResponse:
    return await question_service.get_question(question_id)


@router.delete("/questions/{question_id}")
async def delete_question(
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    question_id: UUID,
) -> dict[UUID, list[UUID]]:
    return await question_service.delete_question(user_id, question_id)
