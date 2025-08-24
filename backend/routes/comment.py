from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.utils import valid_decode_jwt
from database.conf_db import get_async_session
from routes.habits import jwt_token
from schemas.comment import AddCommentSchema, ListHabitsSchema
from schemas.general import SuccessSchema, ErrorSchema
from crud.comment import (
    add_comment_for_habit,
    get_list_comments,
    delete_comment_by_id
)

comment_rout = APIRouter(prefix="/habits", tags=["COMMENT"])


@comment_rout.post(
    "/{habit_id}/comment/",
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def add_habits_comment(
    habit_id: int,
    data: AddCommentSchema,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> SuccessSchema:
    """
    Method adds a comment to the habit.
    """
    await valid_decode_jwt(token.credentials, session)
    await add_comment_for_habit(
        habit_id, data, session
    )
    return SuccessSchema(result=True)


@comment_rout.get(
    "/{habit_id}/comment/",
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorSchema}},
    response_model=ListHabitsSchema,
)
async def get_comment(
    habit_id: int,
    page: int,
    page_size: int = 10,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token),
) -> dict:
    """The method returns a list of comments on the habit."""
    await valid_decode_jwt(token.credentials, session)
    return {
        "data": (
            await get_list_comments(
                habit_id, page, page_size, session
            )
        )
    }


@comment_rout.delete(
    "/comment/{comment_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"model": ErrorSchema}, 404: {"model": ErrorSchema}
    },
    response_model=SuccessSchema
)
async def remove_comment_by_id(
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
    token: HTTPAuthorizationCredentials = Security(jwt_token)
) -> dict:
    """
    Method for deleting comments by ID.
    """
    await valid_decode_jwt(token.credentials, session)
    await delete_comment_by_id(comment_id, session)
    return SuccessSchema(result=True)
