from api.client import Client
from config import register_url, login_url
from utils.login import update_jwt_token


async def registration(data: dict) -> None:
    client: Client = Client(register_url, data)
    await client.post()


async def login_user(data: dict, user_id: int) -> None:
    client: Client = Client(login_url, data)
    response = await client.post()

    await update_jwt_token(response, user_id)
