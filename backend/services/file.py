import json
from pathlib import Path

import aiofiles
import docx2txt
from fastapi import UploadFile
from pydantic import BaseModel


class CreateJson(BaseModel):
    file: str
    data: dict  # BaseModel


# TODO: Директории сейчас не используются
class FileService:
    async def download(self, upload_file: UploadFile):
        # TODO: лишние параметры
        user_file: str = upload_file.filename
        file_title: str = "_".join(
            user_file.split(".")[:-1]
        )  #  Лишние точки заменяются на _
        file_extension: str = user_file.split(".")[-1]
        file_name: str = f"{file_title}.{file_extension}"
        path: str = f"files/{file_title}.{file_extension}"
        content_type: str = upload_file.content_type

        async with aiofiles.open(f"files/{file_title}.{file_extension}", "wb") as file:
            while chunk := await upload_file.read(1024):
                await file.write(chunk)
        return {
            "input": user_file,
            "title": file_title,
            "extension": file_extension,
            "full_name": file_name,
            "path": path,
            "content_type": content_type,
        }

    async def create_json(
        self,
        file_name: str,
        json: BaseModel,
    ) -> CreateJson:
        async with aiofiles.open(
            f"files/{file_name}.json", "w", encoding="utf-8"
        ) as file:
            await file.write(json.model_dump_json())

        return CreateJson(
            file=file_name,
            data=json.model_dump(),
        )

    async def reed_json(self, file_name: str) -> dict:
        async with aiofiles.open(f"files/{file_name}.json", encoding="utf-8") as file:
            data = await file.read()
            data = json.loads(data)
        return data

    async def get_files(self, extension: str = ".docx") -> list[str]:
        """Получить список файлов по расширению"""
        dir = Path("files/")  # TODO: Need async read
        return [item.name for item in dir.iterdir() if item.name.endswith(extension)]

    async def get_text_docx(self, file_title):
        # TODO: need add to reed files with another extensions
        text = docx2txt.process(f"files/{file_title}.docx")
        return text


async def get_file_service() -> FileService:
    return FileService()
