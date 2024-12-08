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
    email: str,
) -> User:
    """
    Находит пользователя по id телеграмм и его username.
    :param email: User's email.
    :param session: AsyncSession
    """
    stmt = select(User).where(User.email == email)
    return await session.scalar(stmt)
