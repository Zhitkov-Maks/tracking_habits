from typing import Tuple

from api.client import Client
from config import register_url, login_url
from utils.login import update_jwt_token


async def registration(data: dict) -> None:
    """
    Вызов клиента для регистрации пользователя.
    :param data: Словарь с данными пользователя.
    """
    client: Client = Client(register_url, data)
    response: Tuple[int, dict] = await client.post()
    if response[0] != 201:
        return response[1].get("detail").get("descr")


async def login_user(data: dict, user_id: int) -> None:
    """
    Вызов клиента для аутентификации.
    :param data: Словарь с данными пользователю
    :param user_id: ID пользователя.
    """
    client: Client = Client(url=login_url, data=data)
    response: Tuple[int, dict] = await client.post()
    if response[0] != 200:
        return response[1].get("detail").get("descr")
    else:
        await update_jwt_token(response, user_id)
