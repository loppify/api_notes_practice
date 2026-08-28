from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UserDao
from app.dao.session_maker import get_session
from app.schemas.user_pd import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(session: AsyncSession = Depends(get_session)):
    return await UserDao.get_all(session)


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    created_user = {**user.model_dump()}
    return await UserDao.add(values=created_user, session=session)

