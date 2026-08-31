import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UserDao
from app.dao.session_maker import get_session

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return UserDao.password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return UserDao.password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(
    username: str, password: str, session: AsyncSession = Depends(get_session)
):
    user = await UserDao.get_user(session, username)

    if not user:
        verify_password(password, UserDao.DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return user
