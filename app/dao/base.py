from typing import Dict, Any, TypeVar, Generic, Union, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.database import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T] = None

    @classmethod
    async def add(cls, session: AsyncSession, values: Union[BaseModel, dict]) -> T:
        if isinstance(values, BaseModel):
            values_dict = values.model_dump(exclude_none=True)
        else:
            values_dict = values
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_all(cls, session: AsyncSession, instances: list[Union[BaseModel, dict]]) -> List[T]:
        if cls.model is None:
            raise ValueError(f"Модель для {cls.__name__} не визначена")
        values_list = [
            item.model_dump(exclude_none=True) if isinstance(item, BaseModel) else item
            for item in instances
        ]
        new_instance = [cls.model(**values) for values in values_list]
        session.add_all(new_instance)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)
        res = await session.execute(query)
        records = res.scalars().all()
        return records
