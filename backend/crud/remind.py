from fastapi import HTTPException
from sqlalchemy import (
    delete,
    Select,
    select,
    Sequence,
    text,
    TextClause,
    Result,
    Delete
)
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.users import Remind, User
from schemas.remind import RemindSchema


async def add_user_time(
    data: RemindSchema,
    user: User,
    session: AsyncSession
) -> None:
    """
    Добавляет настройки для уведомлений.
    :param data: Новое время уведомлений.
    :param user: Пользователь у которого нужно обновить время.
    :param session: Сессия для работы с бд.
    :return None:
    """
    remind: Remind = Remind(
        user_id=user.id,
        time=data.time,
    )
    try:
        session.add(remind)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "result": False,
                "descr": "Напоминание уже существует.",
            },
        )


async def upgrade_time(
    data: RemindSchema,
    user: User,
    session: AsyncSession
) -> None:
    """
    Обновляет время уведомлений.
    :param data: Новое время уведомлений.
    :param user: Пользователь у которого нужно обновить время.
    :param session: Сессия для работы с бд.
    :return None:
    """
    stmt: Select = select(Remind).filter(Remind.user_id == user.id)
    remind: Remind = await session.scalar(stmt)
    if remind is not None:
        remind.time = data.time
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "descr": "Запись не найдена.",
            },
        )

async def remove_time(
    user: User,
    session: AsyncSession
) -> None:
    """
    Удаляет настройки уведомлений.
    :param user: Пользователь которому нужно удалить настройки.
    :param session: Сессия для работы с бд.
    :return None:
    """
    stmt: Delete = delete(Remind).where(Remind.user_id == user.id)
    await session.execute(stmt)
    await session.commit()


async def get_settings_all(session: AsyncSession) -> Sequence:
    """
    Функция возвращает список пользователей у которых
    имеются настройки для уведомлений.
    :param session: AsyncSession
    :return Sequence: Список пользователей и время для показа уведомлений.
    """
    try:
        sql: TextClause = text(
            'SELECT us.user_chat_id, rm.time FROM users as us INNER JOIN '
            'reminds as rm on (us.id = rm.user_id)'
        )
        results: Result = await session.execute(sql)
        return results.all()
    except ProgrammingError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "descr": "Записей еще не создано.",
            },
        )
