from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_comment_keyboard(
    is_another_page: bool, page: int, comment_id
) -> InlineKeyboardMarkup:
    """The function generates a keyboard for the action
    according to a specific habit.
    :return InlineKeyboardMarkup: Use the keyboard to select actions.
    """
    inline_actions: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            ),
            InlineKeyboardButton(
                text="🔙",
                callback_data="show_detail"
            )
        ]
    ]
    if is_another_page:
        inline_actions[0].append(
            InlineKeyboardButton(text=">>", callback_data="next_comment")
        )
    if comment_id:
        inline_actions[0].insert(
            0, InlineKeyboardButton(text="❌", callback_data="remove_comment")
        )
    if page > 1:
        inline_actions[0].insert(
            0, InlineKeyboardButton(text="<<", callback_data="prev_comment")
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)


back_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="🔙", callback_data="show_comments"),
        InlineKeyboardButton(text="К привычке", callback_data="show_detail"),
    ]
]
comment_button = InlineKeyboardMarkup(inline_keyboard=back_button)
