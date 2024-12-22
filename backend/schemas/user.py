from pydantic import BaseModel, EmailStr
from pydantic import Field


class UserData(BaseModel):
    """
    Схема для отправки данных пользователя на сервер.
    Пользователь идентифицируется по email, так как он является
    уникальным для каждого пользователя.
    """
    email: EmailStr = Field(..., description="User's email.")
    password: str = Field(
        ..., min_length=4, description="User's password."
    )


class Email(BaseModel):
    email: str


class ResetPassword(BaseModel):
    new_password: str
    token: str
