from frontend.api.client import Client
from frontend.config import habits_to_update_url
from frontend.utils.create_update import create_header


async def request_update_habit(data: dict, user_id) -> None:
    """Функция для добавления новой привычки."""
    url = habits_to_update_url.format(habit_id=data.get("id"))
    client: Client = Client(url, data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.put()
