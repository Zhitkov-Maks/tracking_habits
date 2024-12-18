from typing import Tuple

from aiohttp.abc import HTTPException

from api.client import Client
from config import remind_url
from utils.create import create_header


async def add_time_remind(data: dict, update: bool, user_id: int) -> None:
    """
    A function for creating a reminder.
    :param data: Data for the save request.
    :param update: Checking changing the record or creating.
    :param user_id: The telegram user ID.
    """
    client: Client = Client(url=remind_url, data=data)
    client.header.update({"Authorization": await create_header(user_id)})
    if not update:
        response: Tuple[int, dict] = await client.post()
    else:
        response: Tuple[int, dict] = await client.patch()

    if response[0] not in (200, 201):
        raise HTTPException(text=response[1].get("detail").get("descr"))


async def remove_time(user_id: int) -> None:
    """
    Request to delete notification.
    :param user_id: The ID of the user to receive the token.
    """
    client: Client = Client(url=remind_url)
    client.header.update({"Authorization": await create_header(user_id)})
    response: Tuple[int, dict] = await client.delete()
    if response[0] != 200:
        raise HTTPException(text=response[1].get("detail").get("descr"))


async def get_all_users() -> dict:
    """
    Retrieves a list with user_chat_id and time for notifications.
    It is necessary to start reminders for all users.
    :return dict: Returns a dictionary with a list of users who have
                    there are settings for notifications.
    """
    client: Client = Client(url=remind_url)
    response: Tuple[int, dict] = await client.get()
    if response[0] == 200:
        return response[1]
