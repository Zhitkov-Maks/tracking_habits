from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.remind import (
    add_user_time,
    upgrade_time,
    remove_time,
    get_settings_all
)
from crud.utils import valid_decode_jwt
from database import User
from database.conf_db import get_async_session
from routes.habits import jwt_token
from schemas.general import SuccessSchema, ErrorSchema
from schemas.remind import RemindSchema, GetRemindSchemaAll

remind = APIRouter(prefix="/remind", tags=["REMIND"])


@remind.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def add_user_remind_database(
    data: RemindSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """Роут добавляет напоминание."""
    user: User = await valid_decode_jwt(token.credentials, session)
    await add_user_time(data, user, session)
    return SuccessSchema(result=True)


@remind.patch(
    "/",
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def update_user_time(
    data: RemindSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    user: User = await valid_decode_jwt(token.credentials, session)
    await upgrade_time(data, user, session)
    return SuccessSchema(result=True)


@remind.delete(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessSchema,
)
async def update_user_time(
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    user: User = await valid_decode_jwt(token.credentials, session)
    await remove_time(user, session)
    return SuccessSchema(result=True)


@remind.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=GetRemindSchemaAll,
)
async def get_settings_time(
    session: AsyncSession = Depends(get_async_session)
) -> GetRemindSchemaAll:
    return GetRemindSchemaAll(users=await get_settings_all(session))
