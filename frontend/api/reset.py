from http.client import HTTPException
from typing import Dict

from api.client import Client
from config import reset_url, reset_password_url, logout_url
from utils.create import create_header


async def get_token_for_reset(email: str) -> Dict[str, str]:
    """
    The function sends an email to verify the existence,
    if there is such an email, then a recovery token is received,
    which is valid for 2 minutes.
    :param email: User's email.
    :return str: Returns the token.
    """
    client: Client = Client(url=reset_url, data={"email": email})
    status_code, response = await client.post()
    if status_code != 201:
        raise HTTPException(response.get("detail").get("descr"))
    return response


async def query_for_reset_password(token: str, new_password: str) -> None:
    """
    A function for sending a password change request.
    If the request was successful, then the password has been changed.
    :param token: Password reset token.
    :param new_password: New password to change.
    :return: None.
    """
    data = {"password": new_password, "token": token}
    client: Client = Client(
        url=reset_password_url,
        data=data
    )
    status_code, response = await client.post()
    if status_code != 201:
        raise HTTPException(response.get("detail").get("descr"))


async def revoke_token(user_id: int):
    """
    A request to revoke the token.
    """
    client: Client = Client(url=logout_url)
    client.header.update(Authorization=await create_header(user_id))
    status_code, response = await client.post()
    if status_code != 204:
        raise HTTPException(response.get("detail").get("descr"))
