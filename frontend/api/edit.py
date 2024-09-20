from api.client import Client
from config import habit_url
from utils.create import create_header


async def request_update_habit(data: dict, user_id) -> None:
    """
    Вызов клиента для обновления привычки.
    :param data: Данные для изменения привычки.
    :param user_id: Id пользователя чата.
    :return None:
    """
    url: str = habit_url + f"{data.get("id")}/"
    client: Client = Client(url=url, data=data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.put()
