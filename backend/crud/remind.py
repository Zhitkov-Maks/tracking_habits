from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.users import Remind
from schemas.remind import RemindSchema


async def add_user_time(
    data: RemindSchema,
    session: AsyncSession
) -> None:
    remind: Remind = Remind(
        user_id=data.user_id,
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
    session: AsyncSession
) -> None:
    remind: Remind | None = await session.get(Remind, data.user_id)
    if remind is not None:
        remind.time = data.time
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "descr": "Запись не найдена.",
            },
        )

async def remove_time(
    data: RemindSchema,
    session: AsyncSession
) -> None:
    stmt = delete(Remind).where(Remind.user_id == data.user_id)
    await session.execute(stmt)
    await session.commit()
