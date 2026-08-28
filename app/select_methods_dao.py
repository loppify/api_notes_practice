# from app.dao.dao import UserDao, TaskDao
#
# from app.dao.session_maker import connection
#
#
# @connection(isolation_level="READ COMMITTED")
# async def select_all_users(session):
#     return await UserDao.get_all(session)
#
# @connection(isolation_level="READ COMMITTED")
# async def select_all_tasks(session):
#     return await TaskDao.get_all(session)
#
