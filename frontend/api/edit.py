from frontend.api.client import Client
from frontend.config import habit_url
from frontend.utils.create import create_header


async def request_update_habit(data: dict, user_id) -> None:
    """Функция для добавления новой привычки."""
    url = habit_url + f"{data.get("id")}/"
    client: Client = Client(url, data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.put()
