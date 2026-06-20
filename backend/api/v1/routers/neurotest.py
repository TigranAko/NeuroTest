import json

import aiofiles
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
    file: FileService = Depends(get_file_service),
) -> dict[str, str]:
    return await file.download(test_file)


@router.get("/files/docx")
async def get_list_docx_files(
    file: FileService = Depends(get_file_service),
) -> list[str]:
    """Получить список всех файлов с расширением .docx (тексты тестов)"""
    return await file.get_files(extension=".docx")


@router.post("/files/json_text")
async def create_json(
    file_title: str,
    text2json: TextToJsonService = Depends(get_text2json_service),
    file: FileService = Depends(get_file_service),
) -> CreateJson:
    """Создать JSON без ответов"""
    text = await file.get_text_docx(file_title)
    questions_without_answers: Test = text2json.parse_test(text)
    data = await file.create_json(file_title + "_text", questions_without_answers)
    return data


@router.get("/files/json_text")
async def get_list_json_text_files(
    file: FileService = Depends(get_file_service),
) -> list[str]:
    """Получить список файлов с расширением .json но без ответов (промежуточные резульатаы)"""
    return await file.get_files(extension="_text.json")


@router.post("/files/json_answer")
async def create_json_answers(
    file_title: str,
    json2answer: JsonToAnswerService = Depends(get_json2answer_service),
    file: FileService = Depends(get_file_service),
) -> TestOutput:
    """Создать JSON с ответами"""
    data = await file.reed_json(file_title + "_text")
    answers: TestOutput = json2answer.process_test(data)
    # answers_str = answers.model_dump_json(indent=4)
    await file.create_json(file_title + "_answers", answers)
    return answers


@router.get("/files/json_answer")
async def get_list_json_anwer_files(
    file: FileService = Depends(get_file_service),
) -> list[str]:
    """Получить список файлов с расширением .json с ответами (Какие тесты уже есть)"""
    return await file.get_files(extension="_answers.json")
