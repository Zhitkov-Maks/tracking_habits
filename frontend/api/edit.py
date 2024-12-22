from http.client import HTTPException

from api.client import Client
from config import habit_url
from utils.create import create_header


async def request_update_habit(data: dict, user_id: int) -> None:
    """
    Request for habit updates.
    :param data: Updated habit data
    :param user_id: Chat user ID.
    """
    url: str = habit_url + f"{data.get("id")}/"
    client: Client = Client(url=url, data=data)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.put()
    if status_code != 200:
        raise HTTPException(response.get("detail").get("descr"))
