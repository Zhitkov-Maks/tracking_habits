from api.client import Client
from config import habit_url
from utils.create import create_header


async def request_create_habit(data: dict, user_id) -> None:
    """Функция для добавления новой привычки."""
    client: Client = Client(habit_url, data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.post()
