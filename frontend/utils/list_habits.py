from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hitalic


async def generate_inline_habits_list(
    habits_list: list
) -> InlineKeyboardMarkup:
    """
    Функция для создания списка активных привычек в виде инлайн клавиатуры.
    """
    inline_habits: list = []
    for obj_habits in habits_list:
        inline_habits.append([
            InlineKeyboardButton(
                text=obj_habits.get("title"),
                callback_data=str(obj_habits.get("id"))
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_habits)


async def generate_message_answer(data: dict) -> str:
    """
    Функция генерирует сообщения для показа
    пользователю его конкретной активной привычки.
    """
    text = (
        f"{hbold(data.get("title"))}\n"
        f"{70*'-'}\n"
        f"{hitalic(data.get("body"))}\n"
        f"Дней отслеживать: {hbold(data.get("number_of_days"))}\n"
        f"Дата начала: {hbold(data.get("start_date")[:10])}\n"
        f"Успешных дней: {hbold(len(data.get("tracking").get("done")))}\n"
        f"Не успешных дней: {hbold(len(data.get("tracking").get("not_done")))}"
    )
    return text
