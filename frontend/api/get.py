from frontend.api.client import Client
from frontend.utils.create import create_header
from frontend.config import habit_url


async def get_list_habits(
    user_id,
    is_active: int = 1
) -> dict:
    url: str = habit_url + f"?is_active={is_active}"
    client: Client = Client(url=url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    return await client.get()


async def get_full_info(
    habit_id: int,
    user_id,
) -> dict:
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url=url)
    client.header.update(
       {"Authorization": await create_header(user_id)}
    )
    return await client.get()


async def delete_habit(
    habit_id: int,
    user_id: int
) -> None:
    url: str = habit_url.format(habit_id=habit_id)
    client: Client = Client(url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.delete()


async def archive_habit(
    habit_id: int,
    user_id: int,
    is_active: bool
) -> None:
    url: str = habit_url.format(habit_id=habit_id)
    client: Client = Client(url=url, data={"is_active": is_active})
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.patch()
