from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from schemas.test_output import TestOutput
from services.test import TestService, get_test_service

router = APIRouter(prefix="/api/v1/tests", tags=["Test"])


@router.get("/all")
async def read_tests(
    test_service: Annotated[TestService, Depends(get_test_service)],
) -> list:
    return await test_service.get_tests()


@router.post("/file")
async def create_test_from_file(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_file: UploadFile,
) -> UUID:
    return await test_service.add_test_from_file(test_file)


@router.put("/file")
async def update_test_from_file(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_file: UploadFile,
    test_id: UUID,
) -> UUID:
    return await test_service.update_test_from_file(test_file, test_id)


@router.post("/")
async def create_test(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_file: TestOutput,
) -> UUID:
    return await test_service.add_test(test_file)


@router.get("/{test_id}")
async def read_test(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_id: UUID,
) -> TestOutput:
    return await test_service.get_test(test_id)


@router.put("/{test_id}")
async def update_test(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test: TestOutput,
    test_id: UUID,
) -> UUID:
    return await test_service.update_test(test, test_id)


@router.delete("/{test_id}")
async def delete_test(
    test_service: Annotated[TestService, Depends(get_test_service)],
    test_id: UUID,
) -> None:
    await test_service.delete_test(test_id)
