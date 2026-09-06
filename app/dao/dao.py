from fastapi.exceptions import RequestValidationError
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.dao.base import BaseDAO
from app.exceptions.custom_exceptions import CREDENTIALS_EXCEPTION
from app.models.tag import Tag
from app.models.task import Task
from app.models.user import User
from app.schemas.user_pd import UserRead


class UserDao(BaseDAO[User]):
    model = User
    password_hash = PasswordHash.recommended()
    DUMMY_HASH = password_hash.hash("dummypassword")

    @classmethod
    async def register(cls, session: AsyncSession, values: BaseModel) -> int:
        v_dict = values.model_dump(exclude_unset=True)
        v_dict["password"] = cls._get_password_hash(v_dict["password"])

        new_user = cls.model(**v_dict)
        session.add(new_user)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()

        new_user = await cls.get_by_id(session, new_user.id)
        return new_user.id

    @classmethod
    def _get_password_hash(cls, password: str) -> str:
        return cls.password_hash.hash(password)

    @classmethod
    async def get_user(cls, session: AsyncSession, username: str | None) -> User | None:
        try:
            stmt = select(cls.model).where(cls.model.username == username)
            res = await session.scalar(stmt)
            return res
        except SQLAlchemyError:
            raise

    @classmethod
    async def delete_user(cls, item_id: int, session: AsyncSession):
        try:
            item = await session.get(cls.model, item_id)
            await session.delete(item)
            await session.commit()
        except UnmappedInstanceError as e:
            raise RequestValidationError("Item not found.") from e

    @classmethod
    async def update_user(
        cls,
        item_id: int,
        session: AsyncSession,
        values: BaseModel,
    ):
        values_dict = values.model_dump(exclude_unset=True)
        try:
            record = await session.get(cls.model, item_id)

            for key, value in values_dict.items():
                if key == "password":
                    value = cls._get_password_hash(value)
                setattr(record, key, value)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return record


class TaskDao(BaseDAO[Task]):
    model = Task

    @classmethod
    async def get_all_tasks(cls, session: AsyncSession, user: UserRead) -> list[Task]:
        res = await session.scalars(
            select(cls.model).where(cls.model.user_id == user.id)
        )
        return list(res.all())

    @classmethod
    async def add(
        cls, session: AsyncSession, values: BaseModel, user: UserRead | None
    ) -> int:
        values_dict = values.model_dump(exclude_unset=True)
        tag_ids: list[int] = values_dict.pop("tag_ids", [])
        if user:
            values_dict["user_id"] = user.id

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
        cls,
        item_id: int,
        session: AsyncSession,
        values: BaseModel,
        user: UserRead | None,
    ) -> Task | None:
        values_dict = values.model_dump(exclude_unset=True)

        tag_ids: list[int] = values_dict.pop("tag_ids", [])
        try:
            record = await session.get(cls.model, item_id)
            if user.id != record.user_id:
                raise CREDENTIALS_EXCEPTION
            for key, value in values_dict.items():
                setattr(record, key, value)
            if tag_ids:
                record.tags = await TagDao.get_by_ids(session=session, items_id=tag_ids)
            else:
                record.tags = []
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.commit()
        return record


class TagDao(BaseDAO[Tag]):
    model = Tag

    @classmethod
    async def get_all_tags(cls, session: AsyncSession) -> list[Tag]:
        res = await session.scalars(select(cls.model))
        return list(res.all())
