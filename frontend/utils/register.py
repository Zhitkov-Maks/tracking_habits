from aiogram.types import Message


async def create_data(message: Message) -> dict:
    """
    Формирует словарь с данными пользователя для сохранения в бд.
    :param message: Сообщение от пользователя с паролем, из него
        так же извлекаем user ID и username.
    :return dict: Возвращает словарь с данными пользователя.
    """
    username: str | None = message.from_user.username

    if username is None:
        username = message.from_user.first_name

    return {
        "username": username,
        "user_chat_id": message.from_user.id,
        "password": message.text
    }
