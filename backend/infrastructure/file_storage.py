import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Literal
from uuid import UUID

import aiofiles
from pydantic import BaseModel
from schemas.test_output import TestOutput


class FileStorage:
    @asynccontextmanager
    async def transaction(
        self,
        test_id: str | UUID,
        mode: Literal["r", "w", "rw"] = "rw",
    ) -> AsyncGenerator[dict, None]:
        data = dict()  # МУТИРУЮЩИЙ объект, для изменения данных
        try:
            if "r" in mode:
                data = await self._read_json(test_id)
            yield data  # При режиме w, data должен мутировать
        except:
            raise
        else:
            if data and "w" in mode:
                test = TestOutput(**data)
                await self._create_json(test, test_id)

    async def _create_json(
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

    async def _read_json(
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
