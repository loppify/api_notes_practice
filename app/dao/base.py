from typing import Dict, Any, TypeVar, Generic, Union, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.database import Base
from app.models.task import Task

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T] = None

    @classmethod
    async def add(cls, session: AsyncSession, values: Union[BaseModel, dict]) -> int:
        if isinstance(values, BaseModel):
            values_dict = values.model_dump(exclude_none=True)
        else:
            values_dict = values.copy()
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
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)
        res = await session.execute(query)
        records = res.scalars().all()
        return records

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        query = select(cls.model).where(cls.model.id == id)
        res = await session.execute(query)
        records = res.scalar_one_or_none()
        return records
