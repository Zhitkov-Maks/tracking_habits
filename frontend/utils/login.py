from config import jwt_token_data


async def update_jwt_token(
    data: dict,
    user_id: int
) -> None:
    jwt_token_data.update({user_id: data})
