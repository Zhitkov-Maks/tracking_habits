from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import create_user
from crud.utils import validate_auth_user
from database.conf_db import get_async_session
from routes.utils import hash_password, encode_jwt
from schemas.general import ErrorSchema, SuccessSchema, TokenSchema
from schemas.user import UserData


user_rout = APIRouter(prefix="/auth", tags=["AUTH"])


@user_rout.post(
    "/registration/",
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorSchema}},
    response_model=SuccessSchema,
)
async def registration_user_rout(
        user: UserData,
        session: AsyncSession = Depends(get_async_session)
) -> SuccessSchema:
    """
    Роут для регистрации пользователя на сервере.
    Обрабатывает входящие данные о пользователе, если все введено
    корректно, то сохраняет пользователя в бд.
    """
    user.password = await hash_password(user.password)
    await create_user(session, user.model_dump())
    return SuccessSchema(result=True)


@user_rout.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorSchema}},
    response_model=TokenSchema,
)
async def auth_user(
    user: UserData = Depends(validate_auth_user),
) -> TokenSchema:
    """
    Роут для аутентификации пользователя. Принимает данные о пользователе,
    проверяет, существует ли такой пользователь, верно ли введен пароль.
    И если все ОК то возвращает токен для последующей аутентификации
    пользователя.
    """
    token: str = await encode_jwt(user)
    return TokenSchema(access_token=token, token_type="Bearer")
