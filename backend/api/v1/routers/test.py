from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.test import TestCreate, TestResponse
from services.test import TestService, get_test_service

router = APIRouter(prefix="/api/v1/tests", tags=["Test"])


@router.post("/")
async def create_test(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_file: TestCreate,
) -> UUID:
    return await test_service.add_test(test_file)


@router.get("/{test_id}")
async def read_test(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_id: UUID,
) -> TestResponse:
    return await test_service.get_test(test_id)
