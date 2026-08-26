from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.tag import Tag
from app.models.task import Task
from app.models.user import User


class UserDao(BaseDAO[User]):
    model = User


class TaskDao(BaseDAO[Task]):
    model = Task


class TagDao(BaseDAO[Tag]):
    model = Tag
