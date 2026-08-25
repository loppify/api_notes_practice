from typing import Dict, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        if cls.model is None:
            raise ValueError(f"Модель для {cls.__name__} не визначена")
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_all(cls, session: AsyncSession, instances: list[Dict[str, Any]]):
        if cls.model is None:
            raise ValueError(f"Модель для {cls.__name__} не визначена")
        new_instance = [cls.model(**values) for values in instances]
        session.add_all(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
