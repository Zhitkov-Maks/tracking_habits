from fastapi import HTTPException
from sqlalchemy import (
    delete,
    Select,
    select,
    Result,
    Delete,
    Sequence
)
from sqlalchemy.exc import IntegrityError
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
    Adds settings for notifications, implemented for telegram users.
    :param data: New notification time.
    :param user: The user who needs to update the time.
    :param session: A session for database queries.
    """
    remind: Remind = Remind(
        user_id=user.id,
        time=data.time,
        user_chat_id=data.user_chat_id
    )
    try:
        session.add(remind)
        await session.commit()
        await session.close()

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
    Updates the notification time.
    :param data: New notification time.
    :param user: The user who needs to update the time.
    :param session: A session for database queries.
    """
    stmt: Select = select(Remind).filter(Remind.user_id == user.id)
    remind: Remind | None = await session.scalar(stmt)
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
    Deletes notification settings.
    :param user: The user who needs to delete the settings.
    :param session: A session for database queries.
    """
    stmt: Delete = delete(Remind).where(Remind.user_id == user.id)
    await session.execute(stmt)
    await session.commit()


async def get_settings_all(session: AsyncSession) -> Sequence:
    """
    The function returns a list of users who have settings.
    for notifications.
    :param session: A session for database queries.
    :return Sequence: The list of users and the time for displaying
                        notifications.
    """
    stmt = select(Remind.user_chat_id, Remind.time)

    results: Result = await session.execute(stmt)
    return results.all()
