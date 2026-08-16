from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from schemas.test_output import TestOutput
from services.file import CreateJson, DownloadFile, FileService, get_file_service
from services.json2answer import (
    JsonToAnswerService,
    get_json2answer_service,
)
from services.jwt import get_current_user_id
from services.text2json import (
    TextToJsonService,
    get_text2json_service,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["LLM"],
)


@router.get("/")
def main():
    return "Hello from NeuroTest!"


@router.post("/files")
async def downloand_user_file(
    test_file: UploadFile,
    file: Annotated[FileService, Depends(get_file_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> DownloadFile:
    # TODO: use user_id for create files
    return await file.download(test_file)


@router.post("/files/json_text")
async def create_json(
    file_title: str,
    text2json: Annotated[TextToJsonService, Depends(get_text2json_service)],
    file: Annotated[FileService, Depends(get_file_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> CreateJson:
    """Создать JSON без ответов"""
    return await text2json.create_json_without_answers(file_title, file, user_id)


@router.post("/files/json_answer")
async def create_json_answers(
    file_title: str,
    json2answer: Annotated[JsonToAnswerService, Depends(get_json2answer_service)],
    file: Annotated[FileService, Depends(get_file_service)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> TestOutput:
    """Создать JSON с ответами"""
    return await json2answer.create_json_answers(file_title, file, user_id)


@router.get("/files")
async def get_files(
    file: Annotated[FileService, Depends(get_file_service)],
    file_type: Literal["docx", "text", "answer"] = "docx",
) -> list[str]:
    """Получить список файлов по типу"""
    return await file.get_files(file_type)
