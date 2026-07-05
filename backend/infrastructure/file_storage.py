import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
from uuid import UUID

import aiofiles
from pydantic import BaseModel
from schemas.test_output import TestOutput


class FileStorage:
    @asynccontextmanager
    async def transaction(
        self,
        test_id: str | UUID,
    ) -> AsyncGenerator[dict, None]:
        try:
            data = await self.read_json(test_id)
            yield data
        except:
            raise
        else:
            test = TestOutput(**data)
            await self.create_json(test, test_id)

    async def create_json(
        self,
        pydantic_data: BaseModel,
        file_name: str | UUID,
        directory: str = "files",
    ) -> dict:
        data: str = pydantic_data.model_dump_json()
        async with aiofiles.open(
            f"{directory}/{file_name}.json",
            "w",
            encoding="utf-8",
        ) as file:
            await file.write(data)
        return {"file": str(file_name), "data": data}

    async def read_json(
        self,
        file_name: str | UUID,
        directory: str = "files",
    ) -> dict:
        async with aiofiles.open(
            f"{directory}/{file_name}.json", encoding="utf-8"
        ) as file:
            data = await file.read()
            data = json.loads(data)
        return data

    async def get_files(
        self,
        directory: str = "files",
    ) -> list[str]:
        """Получить список файлов в директории"""
        dir = Path(f"{directory}/")  # TODO: Need async read
        return [item.name for item in dir.iterdir()]

    async def delete_json(
        self,
        file_name: str | UUID,
        directory: str = "files",
    ) -> None:
        Path(f"{directory}/{file_name}.json").unlink()
