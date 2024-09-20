from api.client import Client
from config import register_url, login_url
from utils.login import update_jwt_token


async def registration(data: dict) -> None:
    """
    Вызов клиента для регистрации пользователя.
    :param data: Словарь с данными пользователя.
    :return dict: Словарь с токеном.
    """
    client: Client = Client(register_url, data)
    await client.post()


async def login_user(data: dict, user_id: int) -> None:
    """
    Вызов клиента для аутентификации.
    :param data: Словарь с данными пользователю
    :param user_id: ID пользователя.
    :return None:
    """
    client: Client = Client(url=login_url, data=data)
    response: dict = await client.post()
    await update_jwt_token(response, user_id)
