from asyncio import run
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UserDao
from app.database import connection


@connection
async def add_one(user_data: dict, session: AsyncSession) -> int:
    new_user = await UserDao.add(session=session, **user_data)
    print("Added new user. ID: ", new_user.id)
    return new_user.id

@connection
async def add_many(user_data: List[dict], session: AsyncSession):
    new_users = await UserDao.add_all(session=session, instances=user_data)
    users_id = [user.id for user in new_users]
    print("Added new user. ID: ", users_id)
    return users_id

users = [
    {"username": "123", "email": "12.34@example.com", "password": "davispassword"},
    {"username": "345", "email": "45.67@example.com", "password": "whiteSecure"},
]
run(add_many(users))