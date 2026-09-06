from collections.abc import Sequence
from typing import Generic, TypeVar

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.dao.database import Base
from app.exceptions.custom_exceptions import (
    CREDENTIALS_EXCEPTION,
    OBJECT_NOT_FOUND_EXCEPTION,
)
from app.schemas.user_pd import UserRead

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def add(
        cls, session: AsyncSession, values: BaseModel, user: UserRead | None
    ) -> int:
        values_dict = values.model_dump(exclude_unset=True)
        values_dict["user_id"] = user.id
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
    async def get_all(cls, user: UserRead, session: AsyncSession) -> list[T]:
        res = await session.scalars(
            select(cls.model).where(cls.model.user_id == user.id)
        )
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
        cls,
        item_id: int,
        session: AsyncSession,
        values: BaseModel,
        user: UserRead | None,
    ) -> T | None:
        values_dict = values.model_dump(exclude_unset=True)
        try:
            record = await session.get(cls.model, item_id)
            if user.id != record.user_id:
                raise CREDENTIALS_EXCEPTION
            for key, value in values_dict.items():
                setattr(record, key, value)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return record

    @classmethod
    async def delete(cls, item_id: int, session: AsyncSession, user: UserRead | None):
        if not user:
            raise CREDENTIALS_EXCEPTION

        user_id = user.id
        try:
            item = await session.get(cls.model, item_id)
            if not item:
                raise OBJECT_NOT_FOUND_EXCEPTION
            if item.user_id != user_id:
                raise CREDENTIALS_EXCEPTION
            await session.delete(item)
            await session.commit()
        except UnmappedInstanceError as e:
            raise RequestValidationError("Item not found.") from e
