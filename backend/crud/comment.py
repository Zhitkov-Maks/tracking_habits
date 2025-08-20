from typing import List

from fastapi import HTTPException
from sqlalchemy import (
    select,
    delete,
    Select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette import status

from database.habits import Comment
from schemas.comment import AddCommentSchema


async def add_comment_for_habit(
    habit_id: int,
    data: AddCommentSchema,
    session: AsyncSession
) -> None:
    """
    Adds comments for habit.
    :param habit_id: The ID of the habit.
    :param data: Data with comment.
    :param session: A session for database queries.
    """
    try:
        comment: Comment = Comment(
            habit_id=habit_id, body=data.body
        )
        session.add(comment)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "descr": f"Запись с идентификатором {habit_id} не найдена."
            }
        )


async def get_list_comments(
    habit_id: int,
    page: int,
    page_size: int,
    session: AsyncSession
) -> List[Comment]:
    """
    Retrieves the list of comments on the habit.
    :param page_size: Page size for the response.
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    :param page: The page you need to display.
    """
    start: int = (page - 1) * page_size
    stmt: Select = (
        select(Comment)
        .filter(Comment.habit_id == habit_id)
        .order_by(Comment.created_at.desc())
        .limit(page_size + 1).offset(start)
    )
    result = await session.scalars(stmt)
    comments = result.all()
    return list(comments)


async def delete_all_comment(
    habit_id: int,
    session: AsyncSession
) -> None:
    """
    Removed all comments
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    """
    stmt = delete(Comment).where(
        Comment.habit_id == habit_id
    )
    await session.execute(stmt)
    await session.commit()


async def delete_comment_by_id(
    comment_id: int,
    session: AsyncSession
) -> None:
    """
    Removed all comments
    :param habit_id: The ID of the habit.
    :param session: A session for database queries.
    """
    comment: Comment | None = await session.get(Comment, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "descr": "Запись не найдена.",
            },
        )
    await session.delete(comment)
    await session.commit()
