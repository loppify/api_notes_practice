from functools import wraps
from typing import Optional
from sqlalchemy import text
from app.dao.database import async_session_maker


def connection(isolation_level: Optional[str] = None, autocommit: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    if isolation_level:
                        await session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
                    result = await func(*args, session=session, **kwargs)
                    if autocommit:
                        await session.commit()
                    return result
                except Exception as e:
                    await session.rollback()
                    raise e
                finally:
                    await session.close()

        return wrapper
    return decorator