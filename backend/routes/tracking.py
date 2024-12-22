from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.check_tracking import correct_tracking, check_count_days_done
from crud.tracking import (
    patch_habit_tracking,
    add_tracking_for_habit,
    check_valid_date
)
from crud.utils import valid_decode_jwt
from database.conf_db import get_async_session
from routes.habits import jwt_token
from schemas.habits import AddTrackSchema
from schemas.general import SuccessSchema, ErrorSchema

track_rout = APIRouter(prefix="/tracking", tags=["TRACKING"])


@track_rout.post(
    "/{habit_id}/",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": ErrorSchema}, 400: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def add_habits_track(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """Роут добавляет отслеживание привычки."""
    await valid_decode_jwt(token.credentials, session)
    await check_valid_date(data, habit_id, session)
    await add_tracking_for_habit(habit_id, data, session)
    await correct_tracking(data.done, habit_id, session)
    if data.done:
        await check_count_days_done(habit_id, session)
    return SuccessSchema(result=True)


@track_rout.patch(
    "/{habit_id}/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessSchema,
)
async def add_habits_track(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """
    Роут изменяет выполнение отслеживания. Например, не
    выполнено на выполнено.
    """
    await valid_decode_jwt(token.credentials, session)
    await check_valid_date(data, habit_id, session)
    await patch_habit_tracking(habit_id, data, session)
    await correct_tracking(data.done, habit_id, session, patch=True)
    if data.done:
        await check_count_days_done(habit_id, session)
    return SuccessSchema(result=True)
