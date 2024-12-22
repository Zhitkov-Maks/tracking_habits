from http.client import HTTPException
from typing import Dict

from api.client import Client
from config import tracking_url
from utils.create import create_header


async def habit_tracking_mark_update(
        data: Dict[str, str | bool], user_id: int
) -> None:
    """
    Updates tracking data for the transmitted day.
    :param data: New tracking information
    :param user_id: Chat user ID
    """
    url: str = tracking_url.format(habit_id=data.get("id"))
    data: dict = {
        "done": True if data.get("done") == "done" else False,
        "date": data.get("date")
    }
    client: Client = Client(url=url, data=data)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.patch()
    if status_code != 200:
        raise HTTPException(response[1].get("detail").get("descr"))


async def habit_tracking_mark(
        data: dict, user_id: int
) -> tuple[int, dict | str]:
    """
    A request to save a mark for a selected day about a
    specific habit.
    :param data: Completed or not completed and the date
    :param user_id: ID user
    :return tuple: Returns the status of the request code and the
                    string if any error occurred
    """
    url: str = tracking_url.format(habit_id=data.get("id"))
    data: dict = {
        "done": True if data.get("done") == "done" else False,
        "date": data.get("date")
    }
    client: Client = Client(url=url, data=data)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.post()

    if status_code == 400:
        raise HTTPException(response.get("detail").get("descr"))

    if status_code == 409:
        response = response.get("detail").get("descr")

    return status_code, response


async def habit_clean_all_tracking(habit_id: int, user_id: int) -> None:
    """
    Clearing all tracking data.
    :param habit_id: The habit ID.
    :param user_id: ID of the chat user
    """
    url: str = tracking_url.format(habit_id=habit_id)

    client: Client = Client(url=url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.delete()
    if status_code != 200:
        raise  HTTPException(response.get("detail").get("descr"))
