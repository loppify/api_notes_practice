from fastapi import APIRouter, status

from app.add_methods_dao import add_one
from app.dao.dao import TaskDao
from app.schemas.task_pd import TaskCreate, TaskRead
from app.schemas.user_pd import UserPydantic
from app.select_methods_dao import select_all_users, select_all_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskCreate):
    created_task = {**task.model_dump()}
    res = await add_one(created_task)
    return res


# @router.get("/")
# async def get_users():
#     all_users = await select_all_users()
#     res = []
#     for i in all_users:`
#         user_pydatnic = UserPydantic.model_validate(i)
#         res.append(user_pydatnic.model_dump())
#     return res

@router.get("/")
async def get_tasks():
    all_tasks = await select_all_tasks()
    res = []
    for i in all_tasks:
        user_pydatnic = TaskRead.model_validate(i)
        res.append(user_pydatnic.model_dump())
    return res
