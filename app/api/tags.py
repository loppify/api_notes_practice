from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import TagDao
from app.dao.session_maker import get_session
from app.schemas.tag_pd import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagRead])
async def get_tags(session: AsyncSession=Depends(get_session)):
    return await TagDao.get_all(session=session)


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_tag(tag: TagCreate, session: AsyncSession=Depends(get_session)):
    created_tag = {**tag.model_dump()}
    return await TagDao.add(values=created_tag, session=session)
