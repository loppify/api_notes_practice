from functools import wraps
from typing import Optional, AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.database import async_session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session