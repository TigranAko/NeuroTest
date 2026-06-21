from typing import Annotated, Literal

from fastapi import APIRouter, Depends, UploadFile
from services.file import CreateJson, FileService, get_file_service
from services.json2answer import (
    JsonToAnswerService,
    TestOutput,
    get_json2answer_service,
)
from services.text2json import (
    Test,
    TextToJsonService,
    get_text2json_service,
)

router = APIRouter(prefix="/api/v1")


@router.get("/")
def main():
    return "Hello from NeuroTest!"


@router.post("/files")
async def downloand_user_file(
    test_file: UploadFile,
    file: Annotated[FileService, Depends(get_file_service)],
) -> dict[str, str]:
    return await file.download(test_file)


@router.post("/files/json_text")
async def create_json(
    file_title: str,
    text2json: Annotated[TextToJsonService, Depends(get_text2json_service)],
    file: Annotated[FileService, Depends(get_file_service)],
) -> CreateJson:
    """Создать JSON без ответов"""
    text = await file.get_text_docx(file_title)
    questions_without_answers: Test = text2json.parse_test(text)
    data = await file.create_json(file_title + "_text", questions_without_answers)
    return data


@router.post("/files/json_answer")
async def create_json_answers(
    file_title: str,
    json2answer: Annotated[JsonToAnswerService, Depends(get_json2answer_service)],
    file: Annotated[FileService, Depends(get_file_service)],
) -> TestOutput:
    """Создать JSON с ответами"""
    data = await file.reed_json(file_title + "_text")
    answers: TestOutput = json2answer.process_test(data)
    # answers_str = answers.model_dump_json(indent=4)
    await file.create_json(file_title + "_answers", answers)
    return answers


@router.get("/files")
async def get_files(
    file: Annotated[FileService, Depends(get_file_service)],
    file_type: Literal["docx", "text", "answer"] = "docx",
) -> list[str]:
    """Получить список файлов по типу"""
    return await file.get_files(file_type)
