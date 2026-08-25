from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.tag import Tag
from app.models.task import Task
from app.models.user import User


class UserDao(BaseDAO):
    model = User

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(cls.model)
        res = await session.execute(query)
        records = res.scalars().all()
        return records


class TaskDao(BaseDAO):
    model = Task


class TagDao(BaseDAO):
    model = Tag
