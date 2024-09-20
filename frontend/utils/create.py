from config import jwt_token_data


async def create_header(user_id: int) -> str:
    """
    Формирование header-а для отправки его в запросе для
    аутентификации пользователя на стороне бэкенда.
    :param user_id: Идентификатор пользователя для получения или создания
        jwt токена.
    :return str: Возвращает строку.
    """
    try:
        token: dict = jwt_token_data[user_id]
        return f"{token.get("token_type")} {token.get("access_token")}"
    except KeyError:
        raise KeyError("Вы не авторизованы!")
