from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_me
from app.dao.dao import UserDao
from app.dao.session_maker import get_session
from app.schemas.responses import UserRead, UserWithTasks
from app.schemas.user_pd import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await UserDao.get_all(session)


@router.get("/{user_id}", response_model=UserWithTasks)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await UserDao.get_by_id(item_id=user_id, session=session)


@router.patch("/", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    data: UserUpdate,
    current_user: Annotated[UserRead, Depends(get_me)],
    session: AsyncSession = Depends(get_session),
):
    return await UserDao.update(current_user.id, session, data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: Annotated[UserRead, Depends(get_me)],
    session: AsyncSession = Depends(get_session),
):

    return await UserDao.delete(user.id, session)
