
from app.dao.dao import UserDao
from app.database import connection
from asyncio import run

from app.schemas.user_pd import UserPydantic


@connection
async def select_all_users(session):
    return await UserDao.get_all_users(session)

all_users = run(select_all_users())
for i in all_users:
    user_pydatnic = UserPydantic.model_validate(i)
    print(user_pydatnic)
