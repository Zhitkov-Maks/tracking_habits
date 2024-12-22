from typing import Dict

from config import jwt_token_data


async def update_jwt_token(
    data: Dict[str, str],
    user_id: int
) -> None:
    """
    Adds a token to the transferred user.
    :param data: Dict with jwt
    :param user_id: ID user.
    :return None:
    """
    jwt_token_data.update({user_id: data})
