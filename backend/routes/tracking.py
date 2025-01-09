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

track_rout = APIRouter(prefix="/habits", tags=["TRACKING"])


@track_rout.post(
    "/{habit_id}/tracking/",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorSchema},
        403: {"model": ErrorSchema},
        409: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def add_habits_track(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """
    The method is intended to add a mark of completion for the
    transferred day.
    """
    await valid_decode_jwt(token.credentials, session)
    await check_valid_date(data, habit_id, session)
    await add_tracking_for_habit(habit_id, data, session)
    await correct_tracking(data.done, habit_id, session)
    if data.done:
        await check_count_days_done(habit_id, session)
    return SuccessSchema(result=True)


@track_rout.patch(
    "/{habit_id}/tracking/",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorSchema},
        403: {"model": ErrorSchema},
        404: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def change_habits_track(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """
    The method is intended to change the completion
    mark for the transferred day.
    """
    await valid_decode_jwt(token.credentials, session)
    await check_valid_date(data, habit_id, session)
    await patch_habit_tracking(habit_id, data, session)
    await correct_tracking(data.done, habit_id, session, patch=True)
    if data.done:
        await check_count_days_done(habit_id, session)
    return SuccessSchema(result=True)
