from pydantic import BaseModel, Field


class SuccessSchema(BaseModel):
    """Схема ответа, если запрос завершился успешно."""

    result: bool


class ErrorSchema(BaseModel):
    """Схема ответа если запрос завершился какой-то ошибкой."""

    result: bool
    descr: str = Field(..., description="Описание ошибки.")


class TokenSchema(BaseModel):
    """Схема для возвращения токена."""

    access_token: str = Field(
        ..., description="Токен для аутентификации."
    )
    token_type: str = Field(
        ...,
        description="Тип всегда будет Bearer, его тоже нужно "
                    "подставлять в headers",
    )


class TokenReset(BaseModel):
    """Схема для возвращения токена."""

    token: str = Field(
        ..., description="Токен для аутентификации."
    )
