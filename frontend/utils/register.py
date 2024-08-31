async def create_data(message) -> dict:
    return {
        "username": message.from_user.username,
        "user_chat_id": message.from_user.id,
        "password": message.text
    }
