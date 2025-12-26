from sre_constants import IN
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext


actions_list = [
    "increase_hours",
    "decrease_hours",
    "increase_minutes",
    "decrease_minutes"
]


async def update_time(action: str, state: FSMContext):
    """
    Update the time depending on the team.
    
    :param action: An action from the user.
    :param state: To save time.
    """
    data = await state.get_data()
    hours, minutes = int(data["hours"]), int(data["minutes"])

    operations = {
        "increase_hours": lambda h, m: ((h + 1) % 24, m),
        "decrease_hours": lambda h, m: ((h - 1) % 24, m),
        "increase_minutes": lambda h, m: (h, (m + 5) % 60),
        "decrease_minutes": lambda h, m: (h, (m - 5) % 60)
    }

    if action in operations:
        hours, minutes = operations[action](hours, minutes)
    
    await state.update_data(hours=hours, minutes=minutes)
    return await create_time(hours, minutes)


async def create_time(hours=12, minutes=0) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard to select the time for notification.
    :return InlineKeyboardMarkup: Returns the keyboard.
    """
    inline_time: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=f"{hours:02d}",
                callback_data="hours"
            ),
            InlineKeyboardButton(
                text=f"{minutes:02d}",
                callback_data="minutes"
            )
        ],
        [
            InlineKeyboardButton(
                text="+",
                callback_data="increase_hours"
            ),
            InlineKeyboardButton(
                text="-",
                callback_data="decrease_hours"
            ),
            InlineKeyboardButton(
                text="+",
                callback_data="increase_minutes"
            ),
            InlineKeyboardButton(
                text="-",
                callback_data="decrease_minutes"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Я выбрал",
                callback_data="save_time"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_time)
