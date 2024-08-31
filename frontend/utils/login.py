from frontend.config import jwt_token_data


async def update_jwt_token(data: dict, user_id: int) -> dict:
    jwt_token_data[user_id] = data
    return jwt_token_data[user_id]
