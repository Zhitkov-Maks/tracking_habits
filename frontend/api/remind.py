from typing import Tuple

from api.client import Client
from config import remind_url
from utils.create import create_header


async def add_time_remind(data: dict, update, user_id) -> str | None:
    """
    Функция для создания записи с настройками напоминания.
    :param data: Данные для сохранения.
    :param update: Проверка изменяем запись или создаем.
    :param user_id: Идентификатор пользователя телеграмм.
    :return None:
    """
    client: Client = Client(url=remind_url, data=data)
    try:
        client.header.update(
            {"Authorization": await create_header(user_id)}
        )
        if not update:
            response: Tuple[int, dict] = await client.post()
        else:
            response: Tuple[int, dict] = await client.patch()

        if response[0] not in (200, 201):
            return response[1].get("detail").get("descr")

    except KeyError:
        return "Вы не авторизованы! 😟😟😟"


async def remove_time(user_id: int) -> None:
    """
    Запрос для удаления настроек получения уведомлений.
    :param user_id: Идентификатор пользователя для получения токена.
    :return None:
    """
    client: Client = Client(url=remind_url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    response: Tuple[int, dict] = await client.delete()
    if response[0] != 200:
        return response[1].get("detail").get("descr")


async def get_all_users() -> dict:
    """
    Получает список с user_chat_id и временем для уведомлений.
    Нужно для запуска напоминаний всех пользователей.
    :return dict: Возвращает словарь со списком пользователей у которых
        есть настройки для уведомлений.
    """
    client: Client = Client(url=remind_url)
    response: Tuple[int, dict] = await client.get()
    if response[0] != 200:
        return response[1].get("detail").get("descr")
