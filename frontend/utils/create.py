from typing import Dict

from config import jwt_token_data


async def create_header(user_id: int) -> str:
    """
    Forming a header to send it in a request for
    user authentication on the backend side.
    :param user_id: ID user.
    :return str: Returns a token for working with requests.
    """
    try:
        token: Dict[str, str] = jwt_token_data[user_id]
        return f"{token.get("token_type")} {token.get("access_token")}"
    except KeyError:
        raise KeyError("Вы не авторизованы!")
