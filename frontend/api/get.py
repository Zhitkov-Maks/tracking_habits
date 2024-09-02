from frontend.api.client import Client
from frontend.utils.create_update import create_header
from frontend.config import (
    get_list_habits_url,
    get_detail_info,
    delete_habit_url,
    habits_to_archive_url
)


async def get_list_habits(user_id) -> dict:
    client: Client = Client(get_list_habits_url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    return await client.get()


async def get_full_info(habit_id: int, user_id) -> dict:
    url: str = get_detail_info + f"{habit_id}/"
    client: Client = Client(url=url)
    client.header.update(
       {"Authorization": await create_header(user_id)}
    )
    return await client.get()


async def delete_habit(habit_id: int, user_id: int) -> None:
    url: str = delete_habit_url.format(habit_id=habit_id)
    client: Client = Client(url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.delete()


async def archive_habit(habit_id: int, user_id: int) -> None:
    url: str = habits_to_archive_url.format(habit_id=habit_id)
    client: Client = Client(url=url, data={"is_active": False})
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.patch()
