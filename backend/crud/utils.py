from fastapi import HTTPException, Depends
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from routes.utils import hash_password, decode_jwt
from crud.user import get_user_by_email
from database import User
from database.conf_db import get_async_session
from schemas.user import UserData, Email


async def validate_auth_user(
    login: UserData,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Verifying the user's existence in the database.
    :param login: User information (email, password).
    :param session: A session for database queries.
    :return User: Returns an instance of the user.
    """
    user: User = await get_user_by_email(session, login.email)
    hash_pass: str = await hash_password(login.password)
    if not user or user.password != hash_pass:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"result": False, "descr": "Неверный email или пароль"},
        )

    return user


async def validate_user_mail(
    email: Email,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Checking the email's existence in the database is needed to
    reset the password.
    :param email: User's email.
    :param session: A session for database queries.
    :return User: Returns an instance of the user.
    """
    user: User = await get_user_by_email(session, email.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"result": False, "descr": "Неверный email или пароль"},
        )

    return user


async def validate_decode_user(
    login: UserData,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Verifying the user's existence in the database.
    :param login: User information (email, password).
    :param session: A session for database queries.
    :return User: Returns an instance of the user.
    """
    user: User = await get_user_by_email(session, login.email)
    if not user or user.password != login.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"result": False, "descr": "Пользователь не найден."},
        )

    return user


async def valid_decode_jwt(token: str, session: AsyncSession) -> User:
    """
    Sends the token for validation and receipt of the user.
    :param token: The transferred token.
    :param session: A session for database queries.
    :return User: Returns an instance of the user.
    """
    try:
        data_user: dict = await decode_jwt(token)
        return await validate_decode_user(UserData(**data_user), session)

    except (DecodeError, ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "detail": False,
                "descr": "Недействительный токен или время работы токена "
                         "истекло.",
            },
        )
