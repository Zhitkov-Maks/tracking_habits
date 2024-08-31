from aiohttp import ClientResponse

from frontend.api.client import Client
from frontend.utils.add_habit import create_header
from frontend.config import get_list_habits_url


async def get_list_habits(user_id) -> list:
    header: str = await create_header(user_id)
    client: Client = Client(get_list_habits_url, {})
    response: dict = await client.get()
    return []