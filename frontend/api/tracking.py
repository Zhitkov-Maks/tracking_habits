from typing import Tuple

from api.client import Client
from config import tracking_url
from utils.create import create_header


async def habit_tracking_mark_update(
    data: dict,
    user_id: int
) -> None:
    url: str = tracking_url.format(habit_id=data.get("id"))
    data: dict = {
        "done": True if data.get("done") == "done" else False,
        "date": data.get("date")
    }
    client: Client = Client(url=url, data=data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    response: Tuple[int, dict] = await client.patch()
    if response[0] != 200:
        return response[1].get("detail").get("descr")


async def habit_tracking_mark(
    data: dict,
    user_id: int
) -> None:
    url: str = tracking_url.format(habit_id=data.get("id"))
    data: dict = {
        "done": True if data.get("done") == "done" else False,
        "date": data.get("date")
    }
    client: Client = Client(url=url, data=data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    response: Tuple[int, dict] = await client.post()
    if response[0] != 201:
        return response[1].get("detail").get("descr")


async def habit_clean_all_tracking(habit_id: int, user_id: int) -> None:
    url: str = tracking_url.format(habit_id=habit_id)

    client: Client = Client(url=url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    response: Tuple[int, dict] = await client.delete()
    if response[0] != 200:
        return response[1].get("detail").get("descr")
