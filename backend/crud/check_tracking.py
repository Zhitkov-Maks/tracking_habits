from datetime import datetime as dt, timedelta

from sqlalchemy import select, func, false, true, Select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tracking import delete_all_habit_tracking
from database import Habit, Tracking


async def check_count_days(
    habit: Habit,
    session: AsyncSession
) -> bool | None:
    """
    The function checks how many days were not completed.
    If the number of such days is more than three, it deletes all
    the marks about the completion. Thus offering to start anew.
    :param habit: A habit that checks the number of days it has been completed.
                    It is needed for changing dates.
    :param session:
    """
    stmt: Select = select(func.count(Tracking.id)).where(
        Tracking.habit_id == habit.id, Tracking.done == false()
    )
    count: int = await session.scalar(stmt)

    if count > 3:
        await delete_all_habit_tracking(habit.id, session)
        habit.start_date = dt.now().date()
        habit.end_date = habit.start_date + timedelta(
            days=habit.number_of_days
        )
    return True


async def add_days_for_tracking(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Changes the end date of the habit by 1 day if received
    a mark of non-fulfillment.
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    """
    habit: Habit | None = await session.get(Habit, habit_id)
    check: bool | None = await check_count_days(habit, session)
    if check:
        habit.end_date = habit.end_date + timedelta(days=1)
    session.add(habit)


async def subtract_days_tracking(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Changes the end date of the habit by -1 day, if received
    a note about the completion of a habit that was marked as not completed.
    :param habit_id:
    :param session: A session for database queries.
    """
    habit: Habit | None = await session.get(Habit, habit_id)

    if (habit.end_date - habit.start_date).days > habit.number_of_days - 1:
        habit.end_date = habit.end_date - timedelta(days=1)
    session.add(habit)


async def correct_tracking(
    done: bool,
    habit_id: int,
    session: AsyncSession,
    patch=False
) -> None:
    """
    Checks whether it is necessary to add or subtract days
    to the tracking end date.
    :param done: Is the habit fulfilled or not fulfilled.
    :param habit_id:
    :param session: A session for database queries.
    :param patch: It is needed if a request has been received
                    to change an already marked day.
    """
    if not done:
        await add_days_for_tracking(habit_id, session)
    elif done and patch:
        await subtract_days_tracking(habit_id, session)
    await session.commit()


async def check_count_days_done(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Checking whether the condition for the number of days
    to track has been met.
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    """
    habit: Habit | None = await session.get(Habit, habit_id)
    stmt: Select = select(func.count(Tracking.id)).where(
        Tracking.habit_id == habit_id, Tracking.done == true()
    )
    count: int = await session.scalar(stmt)
    if count >= habit.number_of_days:
        habit.is_active = False
    await session.commit()
