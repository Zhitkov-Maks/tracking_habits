from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_habit_keyword() -> InlineKeyboardMarkup:
    """
    The function generates a keyboard for the action
    according to a specific habit.
    :return InlineKeyboardMarkup: Use the keyboard to select actions.
    """
    inline_actions = [
        [
            InlineKeyboardButton(
                text="В архив",
                callback_data="archive"
            ),
            InlineKeyboardButton(
                text="Отметить",
                callback_data="mark"
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            )
        ],
        [
            InlineKeyboardButton(
            text="Редактировать",
            callback_data="edit"
        ),
            InlineKeyboardButton(
                text="Список привычек",
                callback_data="show_habits"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)
