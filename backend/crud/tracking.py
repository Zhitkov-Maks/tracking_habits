from datetime import datetime as dt

from fastapi import HTTPException
from sqlalchemy import select, ScalarResult, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import Tracking, Habit
from schemas.habits import AddTrackSchema


async def add_tracking_for_habit(
    habit_id: int,
    data:AddTrackSchema,
    session: AsyncSession
) -> None:
    """
    Добавляет отслеживание за день в базу данных.
    :param habit_id: ID привычки.
    :param data: Данные об отслеживании(Выполнено/Не выполнено)
    :param session: AsyncSession
    """
    try:
        tracking: Tracking = Tracking(
            done=data.done,
            date=dt.date(data.date),
            habit_id=habit_id
        )
        session.add(tracking)
        await session.commit()
    except IntegrityError:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "result": False,
                "descr": "Вы уже добавили запись у данной "
                               "привычки на сегодня."
            },
        )


async def delete_all_habit_tracking(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Удаляет всё отслеживание у конкретной привычки
    :param habit_id: ID Habit
    :param session: AsyncSession
    """
    stmt = delete(Tracking).where(Tracking.habit_id == habit_id)
    await session.execute(stmt)
    await session.commit()


async def tracking_done_by_habit_id(
    habit_id: int,
    done: True | False,
    session: AsyncSession
) -> list:
    """
    Возвращает данные об отслеживании конкретной привычки.
    :param habit_id: ID Habit
    :param done: True или False для получения списка
    выполненных дней и невыполненных дней.
    :param session: AsyncSession
    """
    stmt = (
        select(Tracking)
        .filter(
            Tracking.habit_id == habit_id, Tracking.done == done
        )
    )
    track: ScalarResult[Tracking] = await session.scalars(stmt)
    if track.__sizeof__() == 0:
        return []
    return list(track.unique().all())


async def patch_habit_tracking(
    habit_id: int,
    data: AddTrackSchema,
    session: AsyncSession
) -> None:
    """
    Меняет статус выполнения привычки на текущий день.
    :param habit_id: ID Habit
    :param data: Донные для обновления статуса выполнения отслеживания..
    :param session: AsyncSession
    """
    stmt = (select(Tracking)
            .where(Tracking.date == dt.date(data.date))
            .where(Tracking.habit_id == habit_id))
    tracking: Tracking | None = await session.scalar(stmt)

    if tracking is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "result": False,
            "description": "Запись не найдена."
        },
    )
    tracking.done = data.done
    await session.commit()


async def check_valid_date(
    data: AddTrackSchema,
    habit_id: int,
    session: AsyncSession
) -> None:
    habit: Habit | None = await session.get(Habit, habit_id)
    if habit.start_date > dt.date(data.date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "result": False,
                "descr": "Дата отметки не может быть меньше "
                         "чем дата начала отслеживания."
            },
        )
