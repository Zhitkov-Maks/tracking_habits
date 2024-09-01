from frontend.api.client import Client
from frontend.config import register_url, login_url
from frontend.utils.login import update_jwt_token


async def registration(data: dict) -> dict:
    client: Client = Client(register_url, data)
    result = await client.post()
    if not result.get("result"):
        return result.get("detail").get("description")


async def login_user(data: dict, user_id: int) -> None:
    client: Client = Client(login_url, data)
    response = await client.post()

    await update_jwt_token(response, user_id)
