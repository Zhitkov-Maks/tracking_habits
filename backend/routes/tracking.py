from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.tracking import (
    delete_all_habit_tracking,
    patch_habit_tracking,
    add_tracking_for_habit
)
from crud.utils import valid_decode_jwt
from database.conf_db import get_async_session
from routes.habits import jwt_token
from schemas.habits import AddTrackSchema
from schemas.general import SuccessSchema

track_rout = APIRouter(prefix="/tracking", tags=["TRACKING"])


@track_rout.post(
    "/{habit_id}/add/",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessSchema,
)
async def add_habits_track(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token)
) -> SuccessSchema:
    """Роут добавляет отслеживание привычки."""
    await valid_decode_jwt(token.credentials, session)
    await add_tracking_for_habit(habit_id, data, session)
    return SuccessSchema(result=True)


@track_rout.patch(
    "/{habit_id}/update-status/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessSchema,
)
async def add_habits_track(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token)
) ->SuccessSchema :
    """Роут изменяет выполнение отслеживания. Например, не
    выполнено на выполнено.
    """
    await valid_decode_jwt(token.credentials, session)
    await patch_habit_tracking(habit_id, data, session)
    return SuccessSchema(result=True)


@track_rout.delete(
    "/{habit_id}/delete/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessSchema,
)
async def add_habits_track(
    habit_id: int,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token)
) -> SuccessSchema:
    """
    Роут чтобы, удалить всё отслеживание и начать заново.
    """
    await valid_decode_jwt(token.credentials, session)
    await delete_all_habit_tracking(habit_id, session)
    return SuccessSchema(result=True)
