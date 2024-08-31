import aiohttp
from aiohttp import ClientResponse

from frontend.api.client import Client
from frontend.config import create_habit_url
from frontend.utils.add_habit import create_header


async def request_create_habit(data: dict, user_id) -> str:
    """Функция для добавления новой привычки."""
    client: Client = Client(create_habit_url, data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    response: dict = await client.post()

    if response.get("result"):
        return "Вы добавили привычку. Начинаем отслеживать."
    else:
        return response.get("detail").get("description")
