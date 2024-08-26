from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from routes.utils import hash_password
from crud.user import get_user_by_chat_id
from database import User
from database.conf_db import get_async_session
from schemas.user import UserData


async def validate_auth_user(
    login: UserData,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Функция для проверки существует ли пользователь в базе данных,
    и соответствует ли пароль введенному.
    """
    user: User = await get_user_by_chat_id(
        session, login.user_chat_id, login.username
    )
    hash_pass: str = await hash_password(login.password)
    if not user or user.password != hash_pass:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "result": False,
                "descr": "Пользователь не найден."
            },
        )

    return user
