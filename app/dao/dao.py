from pydantic import BaseModel
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
    async def add(cls, session: AsyncSession, values: BaseModel) -> int:
        values_dict = values.model_dump(exclude_unset=True)
        tag_ids: list[int] = values_dict.pop("tag_ids", [])
        new_task = cls.model(**values_dict)

        if tag_ids:
            new_task.tags = await TagDao.get_by_ids(session=session, items_id=tag_ids)

        session.add(new_task)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return new_task.id

    @classmethod
    async def update(
        cls, item_id: int, session: AsyncSession, values: BaseModel
    ) -> Task | None:
        values_dict = values.model_dump(exclude_unset=True)

        tag_ids: list[int] = values_dict.pop("tag_ids", [])
        try:
            record = await session.get(cls.model, item_id)
            for key, value in values_dict.items():
                setattr(record, key, value)
            if tag_ids:
                record.tags = await TagDao.get_by_ids(session=session, items_id=tag_ids)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return record


class TagDao(BaseDAO[Tag]):
    model = Tag
