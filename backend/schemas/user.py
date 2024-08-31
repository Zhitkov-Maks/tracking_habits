from pydantic import BaseModel
from pydantic import Field


class UserData(BaseModel):
    """
    Схема для отправки данных пользователя на сервер.
    Username и user_chat_id берутся из данных о пользователе в телеграм.
    Пользователь идентифицируется по user_chat_id, так как он является
    уникальным для каждого пользователя телеграмм.
    """
    username: str = Field(..., description="Ваш username из телеграмм.")
    user_chat_id: int = Field(..., description="Чат ай ди из телеграмм.")
    password: str = Field(
        ...,
        min_length=4,
        description="Пароль который ввел пользователь."
    )
