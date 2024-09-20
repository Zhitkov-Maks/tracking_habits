from config import jwt_token_data


async def update_jwt_token(
    data: dict,
    user_id: int
) -> None:
    """
    Добавляет пользователя с его jwt в словарь.
    :param data: Словарь с jwt
    :param user_id: Идентификатор пользователя.
    :return None:
    """
    jwt_token_data.update({user_id: data})
