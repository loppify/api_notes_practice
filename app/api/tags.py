from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import TagDao
from app.dao.session_maker import get_session
from app.schemas.tag_pd import TagCreate, TagReadWithAmount

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_tag(tag: TagCreate, session: AsyncSession = Depends(get_session)):
    return await TagDao.add(values=tag, session=session)


@router.get("/", response_model=list[TagReadWithAmount])
async def get_tags(session: AsyncSession = Depends(get_session)):
    return await TagDao.get_all(session=session)
