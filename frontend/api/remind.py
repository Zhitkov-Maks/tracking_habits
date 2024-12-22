from http.client import HTTPException
from typing import Dict, List

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
    client.header.update(Authorization=await create_header(user_id))
    if not update:
        status_code, response = await client.post()
    else:
        status_code, response = await client.patch()

    if status_code not in (200, 201):
        raise HTTPException(response.get("detail").get("descr"))


async def remove_time(user_id: int) -> None:
    """
    Request to delete notification.
    :param user_id: The ID of the user to receive the token.
    """
    client: Client = Client(url=remind_url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.delete()
    if status_code != 200:
        raise HTTPException(response.get("detail").get("descr"))


async def get_all_users() -> Dict[str, List[Dict[str, int]]]:
    """
    Retrieves a list with user_chat_id and time for notifications.
    It is necessary to start reminders for all users.
    :return dict: Returns a dictionary with a list of users who have
                    there are settings for notifications.
    """
    client: Client = Client(url=remind_url)
    status_code, response = await client.get()
    if status_code == 200:
        return response
