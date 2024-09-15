from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def gen_habit_keyword_archive():
    """
    Функция генерирует клавиатуру для действия
    по конкретной привычке в архиве.
    :return InlineKeyboardButton: Клавиатуру с выбором действий.
    """
    inline_actions: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="Удалить",
                callback_data="delete"
            ),
            InlineKeyboardButton(
                text="Востан-ть",
                callback_data="un_archive"
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)
