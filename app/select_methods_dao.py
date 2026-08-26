from app.dao.dao import UserDao, TaskDao
from asyncio import run

from app.dao.session_maker import connection
from app.schemas.user_pd import UserPydantic


@connection(isolation_level="READ COMMITTED")
async def select_all_users(session):
    return await UserDao.get_all(session)

@connection(isolation_level="READ COMMITTED")
async def select_all_tasks(session):
    return await TaskDao.get_all(session)

# all_users = run(select_all_users())
# for i in all_users:
#     user_pydatnic = UserPydantic.model_validate(i)
#     print(user_pydatnic.model_dump())
