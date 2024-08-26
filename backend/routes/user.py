from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils as auth_utils
from crud.user import create_user
from crud.utils import validate_auth_user
from database.conf_db import get_async_session
from routes.utils import hash_password
from schemas.user import UserData, SuccessSchema, ErrorSchema, TokenSchema

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/jwt/login/",
# )

user_rout = APIRouter(prefix="/auth", tags=["JWT"])


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
    user.password = await hash_password(user.password)
    await create_user(session, user.model_dump())
    return SuccessSchema(result=True)



@user_rout.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorSchema}},
    response_model=TokenSchema
)
def auth_user(
    user: UserData = Depends(validate_auth_user),
) -> TokenSchema:
    jwt_payload = {
        "sub": user.user_chat_id,
        "username": user.username,
        "password": user.password,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenSchema(
        access_token=token,
        token_type="Bearer",
    )
