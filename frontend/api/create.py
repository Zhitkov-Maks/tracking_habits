from frontend.api.client import Client
from frontend.config import create_habit_url
from frontend.utils.create import create_header


async def request_create_habit(data: dict, user_id) -> None:
    """Функция для добавления новой привычки."""
    client: Client = Client(create_habit_url, data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.post()
