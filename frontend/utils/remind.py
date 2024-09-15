from typing import List

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from frontend.api.remind import get_all_users
from frontend.config import BOT_TOKEN, app_schedule, scheduler_ids

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, schedule: AsyncIOScheduler):
        super().__init__()
        self._scheduler = schedule

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


async def create_time() -> InlineKeyboardMarkup:
    """
    Создает инлайн клавиатуру для выбора часа для уведомления.
    :return InlineKeyboardMarkup: Возвращает клавиатуру.
    """
    inline_time: List[List[InlineKeyboardButton]] = []
    for time in range(0, 24, 6):
        inline_time.append(
            [InlineKeyboardButton(text=f"{time + i}", callback_data=str(time+i))
            for i in range(6)
        ])
    inline_time.append(
        [InlineKeyboardButton(text="Я передумал", callback_data="main")]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_time)


async def send_message_cron(user_chat_id: int):
    """
    Отправляет сообщения в нужный чат.
    :param user_chat_id: Идентификатор чата куда посылать оповещение.
    """
    try:
        await bot.send_message(
                user_chat_id,
                "Не забудьте про отслеживание привычек!!!"
            )
    except TelegramForbiddenError:
        # Если пользователь вдруг удалил бота.
        pass


async def get_or_create_scheduler() -> AsyncIOScheduler:
    """
    Функция создает или получает уже созданный экземпляр планировщика
    уведомлений.
    :return AsyncIOScheduler: Экземпляр планировщика.
    """
    if app_schedule.get("scheduler") is None:
        scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        scheduler.start()
        app_schedule["scheduler"] = scheduler
        dp.update.middleware(
            SchedulerMiddleware(schedule=scheduler),
        )
    else:
        scheduler: AsyncIOScheduler = app_schedule["scheduler"]
    return scheduler


async def add_send_message(user_chat_id: int, time: int) -> None:
    """
    Добавляем в scheduler задачи.
    :param user_chat_id: Идентификатор чата куда посылать сообщение.
    :param time: Время выполнения напоминания.
    :return AsyncIOScheduler: Экземпляр планировщика.
    """
    scheduler: AsyncIOScheduler = await get_or_create_scheduler()
    schedule_obj: Job = scheduler.add_job(
        send_message_cron,
        'cron',
        args=[user_chat_id],
        hour=time,
        minute=00,
    )
    scheduler_ids[user_chat_id] = schedule_obj.id


async def create_scheduler_all() -> None:
    """
    Создаем расписание для отправки уведомлений.
    :return: None
    """
    result: dict = await get_all_users()
    for user in result.get("users"):
        await add_send_message(user.get("user_chat_id"), user.get("time"))


async def remove_scheduler_job(user_chat_id: int) -> None:
    """
    Удаляет из планировщика задачу, чтобы затем добавить заново.
    :param user_chat_id: Идентификатор пользователя для получения ID scheduler.
    :return None:
    """
    scheduler: AsyncIOScheduler = await get_or_create_scheduler()
    schedule_id: str = scheduler_ids.get(user_chat_id)
    if schedule_id is not None:
        scheduler.remove_job(schedule_id)
        del scheduler_ids[user_chat_id]
