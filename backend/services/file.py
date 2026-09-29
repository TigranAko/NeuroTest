from pathlib import Path

import aiofiles
import docx2txt
from fastapi import UploadFile
from pydantic import BaseModel


class DownloadFile(BaseModel):
    input: str
    title: str
    content_type: str


# TODO: Директории сейчас не используются
class FileService:
    async def download(self, upload_file: UploadFile) -> DownloadFile:
        user_file: str = upload_file.filename
        file_title: str = "_".join(
            user_file.split(".")[:-1]
        )  #  Лишние точки заменяются на _

        # TODO: Need check extension and type
        file_extension: str = user_file.split(".")[-1]
        content_type: str = upload_file.content_type

        async with aiofiles.open(f"files/{file_title}.{file_extension}", "wb") as file:
            while chunk := await upload_file.read(1024):
                await file.write(chunk)

        return DownloadFile(
            input=user_file,
            title=file_title,
            content_type=content_type,
        )

    async def get_files_docx(
        self,
    ) -> list[str]:
        """Получить список файлов по расширению docx"""
        dir = Path("files/")  # TODO: Need async read
        return [item.name for item in dir.iterdir() if item.name.endswith(".docx")]

    async def get_text_docx(self, file_title):
        # TODO: need add to reed files with another extensions
        text = docx2txt.process(f"files/{file_title}.docx")
        return text


async def get_file_service() -> FileService:
    return FileService()
