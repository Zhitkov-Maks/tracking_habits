from frontend.api.client import Client
from frontend.config import tracking_url
from frontend.utils.create import create_header


async def habit_tracking_mark_update(
    data,
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
    await client.patch()


async def habit_tracking_mark(
    data,
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
    await client.post()



async def habit_clean_all_tracking(habit_id: int, user_id: int) -> None:
    url: str = tracking_url.format(habit_id=habit_id)

    client: Client = Client(url=url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.delete()
