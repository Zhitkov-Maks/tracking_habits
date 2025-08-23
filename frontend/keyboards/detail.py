from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_habit_keyboard() -> InlineKeyboardMarkup:
    """
    The function generates a keyboard for the action
    according to a specific habit.
    :return InlineKeyboardMarkup: Use the keyboard to select actions.
    """
    inline_actions = [
        [
            InlineKeyboardButton(
                text="👉 архив",
                callback_data="archive"
            ),
            InlineKeyboardButton(
                text="✔️",
                callback_data="mark"
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝",
                callback_data="edit"
            ),
            InlineKeyboardButton(
                text="➕",
                callback_data="create_comment"
            ),
            InlineKeyboardButton(
                text="🗒",
                callback_data="show_comments"
            ),
            InlineKeyboardButton(
                text="🔙",
                callback_data="show_habits"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)
