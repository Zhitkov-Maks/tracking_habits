from frontend.config import jwt_token_data



async def create_header(user_id: int) -> str:
    try:
        token: dict = jwt_token_data[user_id]
        return f"{token.get("token_type")} {token.get("access_token")}"
    except KeyError:
        raise KeyError("Вы не авторизованы!")