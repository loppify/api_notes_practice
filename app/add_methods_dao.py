# from typing import List
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.dao.dao import TaskDao, UserDao
#
#
# @connection()
# async def add_one(task_data: dict, session: AsyncSession) -> int:
#     new_task = await TaskDao.add(session=session, values=task_data)
#     return new_task.id
#
# @connection()
# async def add_many(task_data: List[dict], session: AsyncSession):
#     new_tasks = await TaskDao.add_all(session=session, instances=task_data)
#     tasks_id = [task.id for task in new_tasks]
#     return tasks_id
#
# @connection()
# async def add_one_user(user_data: dict, session: AsyncSession) -> int:
#     new_task = await UserDao.add(session=session, values=user_data)
#     return new_task.id