from collections.abc import Sequence
from typing import Generic, TypeVar

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.dao.database import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel) -> int:
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return new_instance.id

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[T]:
        res = await session.scalars(select(cls.model))
        return list(res.all())

    @classmethod
    async def get_by_id(cls, session: AsyncSession, item_id: int):
        try:
            return await session.get(cls.model, item_id)
        except SQLAlchemyError:
            raise

    @classmethod
    async def get_by_ids(
        cls, session: AsyncSession, items_id: Sequence[int]
    ) -> list[T]:
        if not items_id:
            return []
        try:
            stmt = select(cls.model).where(cls.model.id.in_(items_id))
            res = await session.scalars(stmt)
            return list(res.all())
        except SQLAlchemyError:
            raise

    @classmethod
    async def update(
        cls, item_id: int, session: AsyncSession, values: BaseModel
    ) -> T | None:
        values_dict = values.model_dump(exclude_unset=True)
        try:
            record = await session.get(cls.model, item_id)
            for key, value in values_dict.items():
                setattr(record, key, value)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return record

    @classmethod
    async def delete(cls, item_id: int, session: AsyncSession):
        try:
            item = await session.get(cls.model, item_id)
            await session.delete(item)
            await session.commit()
        except UnmappedInstanceError as e:
            raise RequestValidationError("Item not found.") from e
