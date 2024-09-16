from api.client import Client
from utils.create import create_header
from config import habit_url


async def get_list_habits(
    user_id: int,
    is_active: int = 1
) -> dict:
    """
    Запрос на получения списка привычек.
    :param user_id: Идентификатор пользователя телеграмм.
    :param is_active: Нужен, чтобы показывать либо привычки
        из архива либо активные.
    :return dict: Словарь со списком привычек.
    """
    url: str = habit_url + f"?is_active={is_active}"
    client: Client = Client(url=url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    return await client.get()


async def get_full_info(
    habit_id: int,
    user_id: int,
) -> dict:
    """
    Запрос на получения полной информации о конкретной привычке.
    :param habit_id: Идентификатор привычки.
    :param user_id: Идентификатор пользователя телеграмм.
    :return dict: Словарь с полными данными о привычке.
    """
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url=url)
    client.header.update(
       {"Authorization": await create_header(user_id)}
    )
    return await client.get()


async def delete_habit(
    habit_id: int,
    user_id: int
) -> None:
    """
    Запрос на удаление конкретной привычки.
    :param habit_id: Идентификатор привычки.
    :param user_id: Идентификатор пользователя телеграмм.
    :return None:
    """
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.delete()


async def archive_habit(
    habit_id: int,
    user_id: int,
    is_active: bool
) -> None:
    """
    Запрос на изменение статуса привычки.
    :param habit_id: Идентификатор привычки.
    :param user_id: Идентификатор пользователя телеграмм.
    :param is_active: Нужен, чтобы менять статус привычки.
    :return None:
    """
    url: str = habit_url + f"{habit_id}/"
    client: Client = Client(url=url, data={"is_active": is_active})
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.patch()
