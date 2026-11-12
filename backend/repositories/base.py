from typing import Generic, TypeVar
from uuid import UUID

from core.database import Base
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy import ScalarResult, delete, insert, select, update
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: type[ModelType]

    def __init__(self, db: AsyncSession):
        self.db = db

    # async def add_one(
    #     self,
    #     test: TestCreate,
    #     author_id: UUID,
    # ) -> UUID:
    #     data = test.model_dump()
    #     data["author_id"] = author_id
    #     stmt = insert(self.model).values(**data).returning(self.model.id)
    #     user_id = await self.db.execute(stmt)
    #     result = user_id.scalar_one()
    #     return result

    async def get_by_id(self, obj_id: UUID) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        obj = await self.db.execute(stmt)
        return obj.scalar_one_or_none()

    # async def get_all(self) -> ScalarResult[ModelType]:
    #     stmt = select(self.model)
    #     obj = await self.db.execute(stmt)
    #     return obj.scalars()

    async def edit_one(
        self,
        obj_id: UUID,
        obj: CreateSchemaType,
    ) -> UUID:
        data = obj.model_dump()
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(data)
            .returning(self.model.id)
        )
        edited_obj_id = await self.db.execute(stmt)
        result = edited_obj_id.scalar_one()
        return result

    async def partial_edit_one(
        self,
        obj_id: UUID,
        obj: UpdateSchemaType,
    ) -> UUID:
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(obj.model_dump(exclude_unset=True))
            .returning(self.model.id)
        )
        edited_obj_id = await self.db.execute(stmt)
        result = edited_obj_id.scalar_one()
        return result

    async def delete_one(
        self,
        obj_id: UUID,
    ) -> UUID:
        stmt = (
            delete(self.model).where(self.model.id == obj_id).returning(self.model.id)
        )
        obj = await self.db.execute(stmt)
        result = obj.scalar_one()
        return result
