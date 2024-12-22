from typing import Dict, List

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.remind import get_all_users
from config import BOT_TOKEN, app_schedule, scheduler_ids
from keyboards.keyboard import main_menu

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


async def send_message_cron(user_chat_id: int):
    """
    Sends messages to the desired chat.
    :param user_chat_id: The ID of the chat where to send the notification.
    """
    try:
        await bot.send_message(
                user_chat_id,
                "Не забудьте про отслеживание привычек!!!",
                reply_markup=main_menu
            )
    except TelegramForbiddenError:
        # Если пользователь вдруг удалил бота.
        await remove_scheduler_job(user_chat_id)


async def get_or_create_scheduler() -> AsyncIOScheduler:
    """
    The function creates or receives an already created instance
    of the scheduler notifications.
    :return AsyncIOScheduler: An instance of the scheduler.
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
    Adding tasks to the scheduler.
    :param user_chat_id: The ID of the chat where to send the message.
    :param time: The time when the reminder was completed.
    :return AsyncIOScheduler: An instance of the scheduler.
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
    Creating a schedule for sending notifications.
    :return: None
    """
    result: Dict[str, List[Dict[str, int]]] | None = await get_all_users()
    if result:
        for user in result.get("users"):
            await add_send_message(user.get("user_chat_id"), user.get("time"))


async def remove_scheduler_job(user_chat_id: int) -> None:
    """
    Deletes a task from the scheduler in order to add it again.
    :param user_chat_id: The user ID to get the scheduler ID.
    """
    scheduler: AsyncIOScheduler = await get_or_create_scheduler()
    schedule_id: str = scheduler_ids.get(user_chat_id)
    if schedule_id is not None:
        scheduler.remove_job(schedule_id)
        del scheduler_ids[user_chat_id]
