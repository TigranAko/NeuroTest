import logging
from pathlib import Path

import aiofiles
import docx2txt
from fastapi import UploadFile
from pydantic import BaseModel


class DownloadFile(BaseModel):
    input: str
    title: str
    content_type: str


logger = logging.getLogger(__name__)


# TODO: Директории сейчас не используются
class FileService:
    async def download(self, upload_file: UploadFile) -> DownloadFile:
        user_file: str = upload_file.filename
        content_type: str = upload_file.content_type
        logger.info(
            "Saving uploaded file",
            extra={
                "meta": {
                    "filename": user_file,
                    "content_type": content_type,
                },
            },
        )
        file_title: str = "_".join(
            user_file.split(".")[:-1]
        )  #  Лишние точки заменяются на _

        # TODO: Need check extension and type
        file_extension: str = user_file.rsplit(".", maxsplit=1)[-1]

        async with aiofiles.open(f"files/{file_title}.{file_extension}", "wb") as file:
            while chunk := await upload_file.read(1024):
                await file.write(chunk)

        logger.info(
            "File saved successfully",
            extra={
                "meta": {
                    "file_extension": file_extension,
                    "file_title": file_title,
                },
            },
        )
        return DownloadFile(
            input=user_file,
            title=file_title,
            content_type=content_type,
        )

    async def get_files_docx(
        self,
    ) -> list[str]:
        """Получить список файлов по расширению docx"""
        logger.debug("Scanning docx files")
        dir = Path("files/")  # TODO: Need async read
        files = [item.name for item in dir.iterdir() if item.name.endswith(".docx")]
        logger.debug(
            "Scanned docx files",
            extra={"meta": {"count": len(files)}},
        )
        return files

    async def get_text_docx(self, file_title):
        # TODO: need add to reed files with another extensions
        logger.debug(
            "Extracting text from docx",
            extra={
                "meta": {
                    "file_title": file_title,
                },
            },
        )
        text = docx2txt.process(f"files/{file_title}.docx")
        logger.info(
            "Docx text extracted",
            extra={
                "meta": {
                    "file_title": file_title,
                    "text_length": len(text),
                },
            },
        )
        return text


async def get_file_service() -> FileService:
    return FileService()
