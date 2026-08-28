from idlelib import query
from typing import Union, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.tag import Tag
from app.models.task import Task
from app.models.user import User


class UserDao(BaseDAO[User]):
    model = User


class TaskDao(BaseDAO[Task]):
    model = Task

    @classmethod
    async def add(cls, session: AsyncSession, values: Union[BaseModel, dict]) -> int:
        if isinstance(values, BaseModel):
            values_dict = values.model_dump(exclude_none=True)
        else:
            values_dict = values.copy()
        tag_ids: List[int] = values_dict.pop("tag_ids", [])
        new_task = cls.model(**values_dict)
        if tag_ids:
            query = select(Tag).where(Tag.id.in_(tag_ids))
            res = await session.execute(query)
            existing_tags = res.scalars().all()
            new_task.tags = existing_tags

        session.add(new_task)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return new_task.id


class TagDao(BaseDAO[Tag]):
    model = Tag
