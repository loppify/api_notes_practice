from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import TaskDao
from app.dao.session_maker import get_session
from app.schemas.responses import TaskRead
from app.schemas.task_pd import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def get_tasks(session: AsyncSession = Depends(get_session)):
    return await TaskDao.get_all(session=session)


@router.get("/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_task(id: int, session: AsyncSession = Depends(get_session)):
    return await TaskDao.get_by_id(session=session, id=id)


# TODO: finish all necessary endpoints
# @router.patch("/{id}", response_model=TaskUpdate, status_code=status.HTTP_200_OK)
# async def update_task(id: int, task: TaskUpdate, session: AsyncSession = Depends(get_session)):
#     updated_task = {**task.model_dump()}
#     return await TaskDao.update(values=updated_task, session=session, id=id)

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    created_task = {**task.model_dump()}
    return await TaskDao.add(values=created_task, session=session)
