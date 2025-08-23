from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_inline_choice_edit() -> InlineKeyboardMarkup:
    """
    A function to generate a keyboard to select a habit change option.
    :return InlineKeyboardMarkup: An inline keyboard with options.
    """
    inline_edit: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="Название",
                callback_data="edit_title"
            ),
            InlineKeyboardButton(
                text="Описание",
                callback_data="edit_body"
            ),
            InlineKeyboardButton(
                text="Кол-во дней",
                callback_data="edit_period"
            )
        ],
        [
            InlineKeyboardButton(
                text="Полностью",
                callback_data="edit_full"
            ),
            InlineKeyboardButton(
                text="🔙",
                callback_data="show_detail"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_edit)


back_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="🔙", callback_data="edit"),
        InlineKeyboardButton(text="К привычке", callback_data="show_detail"),
    ]
]
edit_button = InlineKeyboardMarkup(inline_keyboard=back_button)
