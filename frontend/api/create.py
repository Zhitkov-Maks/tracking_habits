from typing import Tuple

from api.client import Client
from config import habit_url
from utils.create import create_header


async def request_create_habit(data: dict, user_id: int) -> None:
    """
    Вызов клиента для создания привычки.
    :param data: Данные с привычкой.
    :param user_id: ID пользователя чата.
    :return None:
    """
    client: Client = Client(url=habit_url, data=data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    response: Tuple[int, dict] = await client.post()
    if response[0] != 201:
        return response[1].get("detail").get("descr")
