from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def gen_habit_keyword_archive():
    """
    Функция генерирует клавиатуру для действия
    по конкретной привычке.
    """
    inline_actions = [
        [
            InlineKeyboardButton(
                text="Удалить",
                callback_data="delete"
            ),
            InlineKeyboardButton(
                text="Восстановить",
                callback_data="un_archive"
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)
