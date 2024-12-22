from typing import Tuple, Dict

from api.client import Client
from config import register_url, login_url
from utils.login import update_jwt_token


async def registration(data: Dict[str, str]) -> None:
    """
    Request for user registration.
    :param data: Dictionary with user data.
    """
    client: Client = Client(register_url, data)
    status_code, response = await client.post()
    if status_code != 201:
        return response.get("detail").get("descr")


async def login_user(data: Dict[str, str], user_id: int) -> None:
    """
    The function sends a request for authentication, in case of a
    successful request, we must return a token, which we will
    substitute in all requests in the future.
    :param data: Dictionary with user data.
    :param user_id: ID user.
    """
    client: Client = Client(url=login_url, data=data)
    status_code, response = await client.post()
    if status_code != 200:
        return response.get("detail").get("descr")
    else:
        await update_jwt_token(response, user_id)
