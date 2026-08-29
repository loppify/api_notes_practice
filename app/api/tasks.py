from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import TaskDao
from app.dao.session_maker import get_session
from app.schemas.responses import TaskRead
from app.schemas.task_pd import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    return await TaskDao.get_all(session=session)


@router.get("/{item_id}", response_model=TaskRead)
async def get_task(item_id: int, session: AsyncSession = Depends(get_session)):
    return await TaskDao.get_by_id(session=session, item_id=item_id)


@router.patch(
    "/{item_id}", status_code=status.HTTP_200_OK, response_model=TaskRead | None
)
async def update_task(
    item_id: int, task: TaskUpdate, session: AsyncSession = Depends(get_session)
):
    return await TaskDao.update(item_id=item_id, values=task, session=session)


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    return await TaskDao.add(values=task, session=session)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(item_id: int, session: AsyncSession = Depends(get_session)):
    return await TaskDao.delete(item_id=item_id, session=session)
