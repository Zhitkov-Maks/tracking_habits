from fastapi import APIRouter, status
from fastapi.params import Depends, Security
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy import true, false
from sqlalchemy.ext.asyncio import AsyncSession

from crud.habits import (
    write_habit,
    get_habits_by_user,
    habit_by_id,
    delete_habit_by_id,
    update_habit,
    change_habit_is_active,
)
from crud.tracking import tracking_done_by_habit_id, tracking_for_seven_days
from crud.utils import valid_decode_jwt
from database import User, Habit
from database.conf_db import get_async_session
from schemas.habits import (
    HabitSchema,
    ListHabitsSchema,
    HabitFull,
    ChangeIsActiveSchema,
)
from schemas.general import SuccessSchema, ErrorSchema

habits_router = APIRouter(prefix="/habits", tags=["HABITS"])

jwt_token = HTTPBearer()


@habits_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessSchema,
)
async def create_habits(
    data: HabitSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """Роут обрабатывающий создание новой привычки."""
    user: User = await valid_decode_jwt(token.credentials, session)
    await write_habit(data, user, session)
    return SuccessSchema(result=True)


@habits_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ListHabitsSchema,
)
async def get_list_habits(
    is_active: int,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> dict:
    """
    Роут возвращает список с
    привычками у конкретного пользователя.
    """
    user: User = await valid_decode_jwt(token.credentials, session)
    return {
        "data": (await get_habits_by_user(session, user, bool(is_active)))
        .unique()
        .all()
    }


@habits_router.get(
    "/{habit_id}/",
    status_code=status.HTTP_200_OK,
    response_model=HabitFull,
)
async def get_habits_by_id(
    habit_id: int,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> HabitFull:
    """Роут возвращает полную информацию о привычке."""
    await valid_decode_jwt(token.credentials, session)
    habit: Habit = await habit_by_id(habit_id, session)

    done: int = await tracking_done_by_habit_id(habit_id, true(), session)
    not_done: int = await tracking_done_by_habit_id(habit_id, false(), session)
    seven_days: list = await tracking_for_seven_days(habit_id, session)

    return HabitFull(
        title=habit.title,
        body=habit.body,
        start_date=habit.start_date,
        end_date=habit.end_date,
        is_active=habit.is_active,
        number_of_days=habit.number_of_days,
        tracking={"done": done, "not_done": not_done, "all": seven_days},
    )


@habits_router.delete(
    "/{habit_id}/",
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def delete_habits_track(
    habit_id: int,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """Роут удаляет выбранную привычку."""
    await valid_decode_jwt(token.credentials, session)
    await delete_habit_by_id(habit_id, session)
    return SuccessSchema(result=True)


@habits_router.put(
    "/{habit_id}/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessSchema,
)
async def update_habits_data(
    habit_id: int,
    data: HabitSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """
    Роут изменяет такие данные как название, описание и
    количество дней для отслеживания.
    """
    await valid_decode_jwt(token.credentials, session)
    await update_habit(habit_id, data, session)
    return SuccessSchema(result=True)


@habits_router.patch(
    "/{habit_id}/",
    status_code=status.HTTP_200_OK,
    response_model=SuccessSchema,
)
async def patch_habits_data(
    habit_id: int,
    data: ChangeIsActiveSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """Роут изменяет активность привычки."""
    await valid_decode_jwt(token.credentials, session)
    await change_habit_is_active(habit_id, data, session)
    return SuccessSchema(result=True)
