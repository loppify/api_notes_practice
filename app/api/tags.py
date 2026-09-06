from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_me
from app.dao.dao import TagDao
from app.dao.session_maker import get_session
from app.schemas.tag_pd import TagCreate, TagReadWithAmount, TagUpdate
from app.schemas.user_pd import UserRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_tag(
    tag: TagCreate,
    user: Annotated[UserRead, Depends(get_me)],
    session: AsyncSession = Depends(get_session),
):
    return await TagDao.add(values=tag, session=session, user=user)


@router.get("/", response_model=list[TagReadWithAmount])
async def get_tags(session: AsyncSession = Depends(get_session)):
    return await TagDao.get_all_tags(session=session)


@router.patch("/{item_id}", response_model=TagReadWithAmount)
async def update_tag(
    tag: TagUpdate,
    item_id: int,
    user: Annotated[UserRead, Depends(get_me)],
    session: AsyncSession = Depends(get_session),
):
    return await TagDao.update(values=tag, session=session, item_id=item_id, user=user)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    item_id: int,
    user: Annotated[UserRead, Depends(get_me)],
    session: AsyncSession = Depends(get_session),
):
    return await TagDao.delete(item_id=item_id, session=session, user=user)
