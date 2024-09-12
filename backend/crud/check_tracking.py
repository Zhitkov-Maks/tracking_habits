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
    Функция проверяет сколько дней было не выполнено, и если
    количество таких дней больше трех, то удаляет все отметки о выполнении.
    Тем самым предлагая начать заново.
    :param habit: Привычка у которой проверяем количество дней о выполнении.
        Нужен для изменения дат.
    :param session: AsyncSession для запросов к бд.
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
    Изменяет дату окончания привычки на 1 день, если пришла
    отметка о невыполнении.
    :param habit_id: ID привычки.
    :param session: AsyncSession для запросов к бд.
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
    Изменяет дату окончания привычки на -1 день, если пришла
    отметка о выполнении привычки, которая была помечена как не выполнена.
    :param habit_id: ID привычки.
    :param session: AsyncSession для запросов к бд.
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
    Проверяет нужно ли добавить или отнять дни к дате окончания отслеживания.
    :param done: Выполнена или не выполнена привычка
    :param habit_id: ID привычки.
    :param session: AsyncSession для запросов к бд.
    :param patch: Нужен если запрос пришел на изменение уже отмеченного дня.
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
    Проверяет не выполнено ли количество дней для отслеживания.
    :param habit_id: ID привычки.
    :param session: AsyncSession для запросов к бд.
    """
    habit: Habit | None = await session.get(Habit, habit_id)
    stmt: Select = select(func.count(Tracking.id)).where(
        Tracking.habit_id == habit_id, Tracking.done == true()
    )
    count: int = await session.scalar(stmt)
    if count >= habit.number_of_days:
        habit.is_active = False
    await session.commit()
