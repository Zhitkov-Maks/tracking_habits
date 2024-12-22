from typing import Tuple

from fastapi import HTTPException
from sqlalchemy import select, Select, Update, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import User
from routes.utils import hash_password
from schemas.user import ResetPassword


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


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User:
    """
    Находит пользователя по id телеграмм и его username.
    :param email: User's email.
    :param session: AsyncSession
    """
    stmt: Select[Tuple[User]] = select(User).where(User.email == email)
    return await session.scalar(stmt)


async def update_user_password(
    email: str,
    reset_password: ResetPassword,
    session: AsyncSession
) -> None:
    password = await hash_password(reset_password.new_password)
    stmt: Update = (
        update(User)
        .where(User.email == email)
        .values(password=password)
    )
    await session.execute(stmt)
    await session.commit()
