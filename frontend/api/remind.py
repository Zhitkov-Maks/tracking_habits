from frontend.api.client import Client
from frontend.config import remind_url
from frontend.utils.create import create_header


async def add_time_remind(data: dict, update, user_id) -> None:
    """
    Функция для создания записи с настройками напоминания.
    :param data: Данные для сохранения.
    :param update: Проверка изменяем запись или создаем.
    :param user_id: Идентификатор пользователя телеграмм.
    :return None:
    """
    client: Client = Client(remind_url, data)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    if not update:
        await client.post()
    else:
        await client.patch()


async def remove_time(user_id: int) -> None:
    """
    Запрос для удаления настроек получения уведомлений.
    :param user_id: Идентификатор пользователя для получения токена.
    :return None:
    """
    client: Client = Client(remind_url)
    client.header.update(
        {"Authorization": await create_header(user_id)}
    )
    await client.delete()


async def get_all_users() -> dict:
    """
    Получает список с user_chat_id и временем для уведомлений.
    Нужно для запуска напоминаний всех пользователей.
    :return dict: Возвращает словарь со списком пользователей у которых
        есть настройки для уведомлений.
    """
    url: str = remind_url + "list/"
    client: Client = Client(url)
    return await client.get()
