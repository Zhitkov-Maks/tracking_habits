from datetime import timedelta, datetime
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


weekdays: dict[int, str] = {0: "Сегодня", 1: "Вчера", 2: "Позавчера"}


async def get_weekdays() -> dict:
    """
    Gets the date and day of the week to add a mark of
    completion/non-fulfillment.
    :return dict: The dictionary where the key is the number of days ago,
                    and the value is a tuple with the date and day of the week.
    """
    today: datetime.date = datetime.now().date()
    days: list = []
    for i in range(7):
        curr_date = today - timedelta(days=i)
        days.append((
            f"{str(curr_date)[8:10]}.{str(curr_date)[5:7]}",
            weekdays[curr_date.weekday()]
        ))
    return days


async def inline_choice_calendar(days_ago: int) -> InlineKeyboardMarkup:
    """
    Generates a keyboard with dates to mark the completion/non-fulfillment.
    :return InlineKeyboardMarkup: A keyboard with dates.
    """
    inline_choice: list[list[InlineKeyboardButton]] = []
    date_for_mark = datetime.now().date() - timedelta(days_ago)

    if days_ago in weekdays:
        inline_choice.append(
            [
                InlineKeyboardButton(
                    text=weekdays[days_ago] + " ❓",
                    callback_data=str(date_for_mark)
                )
            ]
        )
    else:
        inline_choice.append(
            [
                InlineKeyboardButton(
                    text=f"{date_for_mark} ?",
                    callback_data=str(date_for_mark)
                )
            ]
        )

    inline_choice.append(
        [
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            ),
            InlineKeyboardButton(
                text="🔙",
                callback_data="show_detail"
            ),
            InlineKeyboardButton(
                text=">>",
                callback_data="prev_day"
            ),
        ]
    )
    if days_ago > 0:
        inline_choice[1].insert(0, InlineKeyboardButton(
            text="<<",
            callback_data="next_day"
        ))
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
                text="🔙", callback_data="show_detail"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=choice)
