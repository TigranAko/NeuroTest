from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.test_output import AnswerOutput
from services.answer import AnswerService, get_answer_service

router = APIRouter(
    prefix="/api/v1/tests/{test_id}/answers",
    tags=["Answer"],
)


@router.post("/")
async def create_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    answer: AnswerOutput,
    test_id: UUID,
    question_id: UUID | int = 0,
    answer_id: int = 0,
) -> UUID:
    return await question_service.add_answer(answer, test_id, question_id, answer_id)


@router.get("/")
async def read_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    test_id: UUID,
    question_id: UUID | int = 0,
    answer_id: int = 0,
) -> AnswerOutput:
    return await question_service.get_answer(test_id, question_id, answer_id)


@router.put("/")
async def update_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    answer: AnswerOutput,
    test_id: UUID,
    question_id: UUID | int = 0,
    answer_id: int = 0,
) -> UUID:
    return await question_service.update_answer(answer, test_id, question_id, answer_id)


@router.delete("/")
async def delete_answer(
    question_service: Annotated[AnswerService, Depends(get_answer_service)],
    test_id: UUID,
    question_id: UUID | int = 0,
    answer_id: int = 0,
) -> None:
    await question_service.delete_answer(test_id, question_id, answer_id)
