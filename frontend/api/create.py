from typing import Dict
from http.client import HTTPException

from api.client import Client
from config import habit_url
from utils.create import create_header


async def request_create_habit(data: Dict[str, str], user_id: int) -> None:
    """
    Sends a request to create a habit.
    :param data: A dictionary with data to create a habit.
    :param user_id: ID user.
    :return str: If the request was not successful, then we return an
                    error string.
    """
    client: Client = Client(url=habit_url, data=data)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.post()
    if status_code != 201:
        raise HTTPException(response.get("detail").get("descr"))
