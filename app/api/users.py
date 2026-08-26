from fastapi import APIRouter, status

from app.add_methods_dao import add_one, add_one_user
from app.dao.dao import TaskDao
from app.schemas.task_pd import TaskCreate
from app.schemas.user_pd import UserPydantic
from app.select_methods_dao import select_all_users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_user(task: UserPydantic):
    created_task = {**task.model_dump()}
    res = await add_one_user(created_task)
    return res


@router.get("/")
async def get_users():
    all_users = await select_all_users()
    res = []
    for i in all_users:
        user_pydatnic = UserPydantic.model_validate(i)
        res.append(user_pydatnic.model_dump())
    return res
