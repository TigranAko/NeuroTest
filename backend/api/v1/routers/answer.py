from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.answer import AnswerCreate, AnswerResponse
from services.answer import AnswerService, get_answer_service
from services.jwt import get_current_user_id

router = APIRouter(
    prefix="/api/v1",
    tags=["Answer"],
)


@router.post("/questions/{question_id}/answers")
async def create_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    answer: AnswerCreate,
    question_id: UUID,
) -> UUID:
    return await question_service.add_answer(user_id, answer, question_id)


@router.get("/questions/{question_id}/answers")
async def read_answers_question(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    question_id: UUID,
) -> list[AnswerResponse]:
    return await question_service.get_answers_question(question_id)


@router.get("/answers/{answer_id}")
async def read_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    answer_id: UUID,
) -> AnswerResponse:
    return await question_service.get_answer(answer_id)


@router.delete("/answers/{answer_id}")
async def delete_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    answer_id: UUID,
) -> UUID:
    return await question_service.delete_answer(user_id, answer_id)
