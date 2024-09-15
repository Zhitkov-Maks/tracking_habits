async def create_data(message) -> dict:
    username: str | None = message.from_user.username

    if username is None:
        username = message.from_user.first_name

    return {
        "username": username,
        "user_chat_id": message.from_user.id,
        "password": message.text
    }
