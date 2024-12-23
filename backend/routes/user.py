import asyncio
from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from config import SUBJECT, BODY
from crud.user import create_user, update_user_password
from crud.utils import validate_auth_user, validate_user_mail, valid_decode_jwt
from database import User
from database.conf_db import get_async_session
from routes.utils import hash_password, encode_jwt, send_email
from schemas.general import ErrorSchema, SuccessSchema, TokenSchema, TokenReset
from schemas.user import UserData, ResetPassword

user_rout = APIRouter(prefix="/auth", tags=["AUTH"])


@user_rout.post(
    "/registration/",
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def registration_user_rout(
        user: UserData,
        session: AsyncSession = Depends(get_async_session)
) -> SuccessSchema:
    """This method is used to register a user on the server."""
    user.password = await hash_password(user.password)
    await create_user(session, user.model_dump())
    return SuccessSchema(result=True)


@user_rout.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorSchema}},
    response_model=TokenSchema,
)
async def auth_user(
    user: UserData = Depends(validate_auth_user),
) -> TokenSchema:
    """The method is designed to authenticate the user and issue him a token."""
    token: str = await encode_jwt(user)
    return TokenSchema(access_token=token, token_type="Bearer")


@user_rout.post(
    "/request-password-reset/",
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorSchema}},
)
async def request_password_reset(
        user: UserData = Depends(validate_user_mail)
) -> TokenReset:
    """The method is designed to issue a password reset token."""
    token: str = await encode_jwt(user, expire_timedelta=timedelta(minutes=1))
    return TokenReset(token=token)


@user_rout.post(
    "/reset-password/",
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorSchema}},
)
async def reset_password(
    reset_data: ResetPassword,
    session: AsyncSession = Depends(get_async_session),
) -> SuccessSchema:
    """
    The method is designed to change the user's password and
    email him.
    """
    user: User = await valid_decode_jwt(reset_data.token, session)
    await update_user_password(user.email, reset_data, session)
    asyncio.create_task(send_email(user.email, SUBJECT, BODY))
    return SuccessSchema(result=True)
