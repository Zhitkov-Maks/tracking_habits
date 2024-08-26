from pydantic import BaseModel
from pydantic import Field


class SuccessSchema(BaseModel):
    result: bool


class ErrorSchema(BaseModel):
    result: bool
    descr: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserData(BaseModel):
    username: str
    user_chat_id: int
    password: str = Field(..., min_length=8)


class ReturnUserSchema(BaseModel):
    """Schema for adding tweet."""

    response: bool = Field(..., description="Result, true or false")
    data: UserData = Field(..., description="Данные пользователя")