from datetime import datetime as dt, timedelta, datetime

from fastapi import HTTPException
from sqlalchemy import select, ScalarResult, true, false, True_, False_, Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.tracking import delete_all_habit_tracking
from database import Habit, User
from schemas.habits import HabitSchema, ChangeIsActiveSchema


async def change_habit_is_active(
    habit_id: int,
    data: ChangeIsActiveSchema,
    session: AsyncSession
) -> None:
    """
    Changes the status of the habit. If there is a recovery from the archive,
    then all previous tracking is deleted, and the start and
    end dates are changed.
    :param habit_id: The ID of the habit.
    :param data: Data for changing the status of a habit.
    :param session: A session for database queries.
    """
    habit: Habit | None = await session.get(Habit, habit_id)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "description": "Привычка не найдена, возможно она уже удалена.",
            },
        )
    habit.is_active = data.is_active

    if data.is_active:
        await delete_all_habit_tracking(habit_id, session)
        habit.start_date = dt.now().date()
        habit.end_date = (
                dt.now() + timedelta(days=habit.number_of_days - 1)
        ).date()
    await session.commit()


async def update_habit(
    habit_id: int,
    data: HabitSchema,
    session: AsyncSession
) -> None:
    """
    Changes all the data about the habit.
    :param habit_id: The ID of the habit.
    :param data: Data for habit updates.
    :param session: A session for database queries.
    """
    habit: Habit | None = await session.get(Habit, habit_id)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "description": "Привычка не найдена, возможно она уже удалена.",
            },
        )
    habit.title = data.title
    habit.body = data.body
    habit.number_of_days = data.number_of_days
    habit.end_date = habit.start_date + timedelta(days=data.number_of_days - 1)
    await session.commit()


async def delete_habit_by_id(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Deletes a habit from the database.
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    """
    habit: Habit | None = await session.get(Habit, habit_id)
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "descr": "Привычка не найдена, возможно она уже удалена.",
            },
        )
    await session.delete(habit)
    await session.commit()


async def habit_by_id(
    habit_id: int,
    session: AsyncSession
) -> Habit:
    """
    We get a habit by its identifier.
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    :return Habit: Brings back the habit.
    """
    stmt: Select = select(Habit).where(Habit.id == habit_id)
    habit: Habit | None = await session.scalar(stmt)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "description": "Привычка не найдена, попробуйте еще раз.",
            },
        )
    return habit


async def write_habit(
    data: HabitSchema,
    user: User,
    session: AsyncSession
) -> None:
    """
    Adds a habit to the database.
    :param data: Habit data to be recorded in the database
    :param user: User Instance.
    :param session: A session for database queries.
    """
    end_date: datetime.date = (dt.now().date() +
                               timedelta(days=data.number_of_days - 1))
    habit: Habit = Habit(
        user_id=user.id,
        title=data.title,
        body=data.body,
        number_of_days=data.number_of_days,
        start_date=datetime.now().date(),
        end_date=end_date,
    )
    session.add(habit)
    await session.commit()


async def get_habits_by_user(
    session: AsyncSession, user: User, is_active: bool
) -> ScalarResult[Habit]:
    """
    Returns a list of habits for a specific user.
    :param session: A session for database queries.
    :param user: User Instance.
    :param is_active: Show active or already inactive habits.
    :return ScalarResult[Habit]: Returns a list of the user's habits.
    """
    active: True_ | False_ = true() if is_active else false()
    stmt = (
        select(Habit)
            .where(
        Habit.user_id == user.id, Habit.is_active == active
        )
    )
    return await session.scalars(stmt)
