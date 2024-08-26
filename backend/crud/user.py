from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import User


async def create_user(session: AsyncSession, user: dict) -> None:
    """Записывает пользователя в бд."""
    user: User = User(**user)
    try:
        session.add(user)
        await session.commit()
        await session.close()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "result": False,
                "description": "Пользователь с таким именем "
                               "уже зарегистрирован."
            },
        )


async def get_user_by_chat_id(
    session: AsyncSession,
    chat_id: int,
    username: str
) -> User:
    """Находит пользователя по chat_id и username."""
    stmt = select(User).where(
        User.user_chat_id == chat_id
    ).where(User.username == username)
    return await session.scalar(stmt)
