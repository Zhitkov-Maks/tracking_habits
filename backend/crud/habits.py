from fastapi import HTTPException
from sqlalchemy import select, ScalarResult, true, false, True_, False_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import Habit, User
from schemas.habits import HabitSchema, ChangeIsActiveSchema


async def change_habit_is_active(
    habit_id: int,
    data: ChangeIsActiveSchema,
    session: AsyncSession
) -> None:
    """
    Изменяет статус привычки.
    :param habit_id: ID Habit
    :param data: Донные для изменения статуса привычки.
    :param session: AsyncSession
    """
    habit: Habit | None= await session.get(Habit, habit_id)
    if habit is None:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "result": False,
            "description": "Привычка не найдена, возможно она уже удалена."
        },
    )
    habit.is_active = data.is_active
    await session.commit()


async def update_habit(
    habit_id: int,
    data: HabitSchema,
    session: AsyncSession
) -> None:
    """
    Изменяет все данные о привычке.
    :param habit_id: ID Habit
    :param data: Донные для обновления привычки.
    :param session: AsyncSession
    """
    habit: Habit | None= await session.get(Habit, habit_id)
    if habit is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "result": False,
            "description": "Привычка не найдена, возможно она уже удалена."
        },
    )
    habit.title = data.title
    habit.body = data.body
    habit.number_of_days = data.number_of_days
    await session.commit()


async def delete_habit_by_id(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Удаляет привычку из базу данных.
    :param habit_id: ID Habit
    :param session: AsyncSession
    """
    habit: Habit | None= await session.get(Habit, habit_id)
    if habit is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "result": False,
            "descr": "Привычка не найдена, возможно она уже удалена."
        },
    )
    await session.delete(habit)
    await session.commit()


async def habit_by_id(
    habit_id: int,
    session: AsyncSession
) -> Habit:
    """
    Получаем привычку по ее идентификатору.
    :param habit_id: ID habit's
    :param session: AsyncSession
    :return Habit: Возвращает привычку.
    """
    stmt = (
        select(Habit)
        .where(Habit.id == habit_id)
    )
    habit: Habit | None = await session.scalar(stmt)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "description": "Привычка не найдена, попробуйте еще раз."
            },
        )
    return habit


async def write_habit(
    data: HabitSchema,
    user: User,
    session: AsyncSession
) -> None:
    """
    Добавляет привычку в базу данных.
    :param data: Данные о привычке для записи в бд
    :param user: Экземпляр User
    :param session: AsyncSession
    """
    habit: Habit = Habit(
        user_id=user.id,
        title=data.title,
        body=data.body,
    )
    session.add(habit)
    await session.commit()


async def get_habits_by_user(
    session: AsyncSession,
    user: User,
    is_active: bool
) -> ScalarResult[Habit]:
    """
    Возвращает список привычек для конкретного пользователя.
    :param session: AsyncSession
    :param user: Экземпляр User.
    :param is_active: Показать активные или уже неактивные привычки.
    :return ScalarResult[Habit]: Возвращает список привычек пользователя.
    """
    archive: True_ | False_ = true() if is_active else false()
    stmt = (select(Habit)
            .where(
        Habit.user_id == user.id,
        Habit.is_active == archive)
    )
    return await session.scalars(stmt)
