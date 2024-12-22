from datetime import timedelta, datetime
from typing import Dict, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


weekdays: tuple = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс",)

async def get_weekdays() -> dict:
    """
    Gets the date and day of the week to add a mark of
    completion/non-fulfillment.
    :return dict: The dictionary where the key is the number of days ago,
                    and the value is a tuple with the date and day of the week.
    """
    today: datetime.date = datetime.now().date()
    days: Dict[int, tuple] = {}
    for i in range(7):
        curr_date = today - timedelta(days=i)
        days.update({i: (
            f"{str(curr_date)[8:10]}.{str(curr_date)[5:7]}",
            weekdays[curr_date.weekday()]
        )})
    return days


async def inline_choice_calendar() -> InlineKeyboardMarkup:
    """
    Generates a keyboard with dates to mark the completion/non-fulfillment.
    :return InlineKeyboardMarkup: A keyboard with dates.
    """
    days: dict = await get_weekdays()
    inline_choice = [
        [
            InlineKeyboardButton(
                text=str(days[0][0]) + f"({days[0][1]})",
                callback_data="zero"
            ),
            InlineKeyboardButton(
                text=str(days[1][0]) + f"({days[1][1]})",
                callback_data="one"
            ),
            InlineKeyboardButton(
                text=str(days[2][0]) + f"({days[2][1]})",
                callback_data="two"
            ),
            InlineKeyboardButton(
                text=str(days[3][0]) + f"({days[3][1]})",
                callback_data="three"
            ),
        ],
        [
            InlineKeyboardButton(
                text=str(days[4][0]) + f"({days[4][1]})",
                callback_data="four"
            ),
            InlineKeyboardButton(
                text=str(days[5][0]) + f"({days[5][1]})",
                callback_data="five"
            ),
            InlineKeyboardButton(
                text=str(days[6][0]) + f"({days[6][1]})",
                callback_data="six"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_choice)


async def inline_done_not_done() -> InlineKeyboardMarkup:
    """
    Create a keyboard to add a mark of completion or non-completion.
    :return InlineKeyboardMarkup: Returns the keyboard.
    """
    choice: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="✅", callback_data="done"
            ),
            InlineKeyboardButton(
                text="❌", callback_data="not_done"
            ),
            InlineKeyboardButton(
                text="Отмена", callback_data="main"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=choice)
