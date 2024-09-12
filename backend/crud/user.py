from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import User


async def create_user(session: AsyncSession, user: dict) -> None:
    """
    Создает пользователя в базе данных.
    :param user: Словарь с данными о пользователе.
    :param session: AsyncSession
    """
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
                "descr": "Пользователь с текущими данными уже зарегистрирован.",
            },
        )


async def get_user_by_id_and_username(
    session: AsyncSession,
    chat_id: int,
    username: str
) -> User:
    """
    Находит пользователя по id телеграмм и его username.
    :param chat_id: ID чата телеграмм.
    :param username: Username пользователя
    :param session: AsyncSession
    """
    stmt = (
        select(User)
        .where(User.user_chat_id == chat_id)
        .where(User.username == username)
    )
    return await session.scalar(stmt)
