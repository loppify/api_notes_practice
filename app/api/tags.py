from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import TagDao
from app.dao.session_maker import get_session
from app.schemas.tag_pd import TagCreate, TagReadWithAmount, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_tag(tag: TagCreate, session: AsyncSession = Depends(get_session)):
    return await TagDao.add(values=tag, session=session)


@router.get("/", response_model=list[TagReadWithAmount])
async def get_tags(session: AsyncSession = Depends(get_session)):
    return await TagDao.get_all(session=session)


@router.patch("/{item_id}", response_model=TagReadWithAmount)
async def update_tag(
    tag: TagUpdate, item_id: int, session: AsyncSession = Depends(get_session)
):
    return await TagDao.update(values=tag, session=session, item_id=item_id)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(item_id: int, session: AsyncSession = Depends(get_session)):
    return await TagDao.delete(item_id=item_id, session=session)