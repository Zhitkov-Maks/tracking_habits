from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_time() -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard to select the time for notification.
    :return InlineKeyboardMarkup: Returns the keyboard.
    """
    inline_time: List[List[InlineKeyboardButton]] = []
    for time in range(0, 24, 6):
        inline_time.append(
            [
                InlineKeyboardButton(
                    text=f"{time + i}",
                    callback_data=str(time+i)) for i in range(6)
            ]
            )
    inline_time.append(
        [InlineKeyboardButton(text="Отмена", callback_data="main")]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_time)
