from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_bot: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="В процессе 📈",
                callback_data="show_habits"
            )
        ],
        [
            InlineKeyboardButton(
                text="Архив 👉 🗄.",
                callback_data="show_archive"
            )
        ],
        [
            InlineKeyboardButton(
                text="👀",
                callback_data="show_commands"
            ),
            InlineKeyboardButton(
                text="➕",
                callback_data="create"
            ),
            InlineKeyboardButton(
                text="🔐",
                callback_data="auth"
            ),
            InlineKeyboardButton(
                text="💤",
                callback_data="remind"
            )
        ],
        [
            InlineKeyboardButton(
                text="Выйти из аккаунта",
                callback_data="clear_history"
            )
        ]
    ]


cancel_button: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

confirm_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Да", callback_data="yes"),
        InlineKeyboardButton(text="Нет", callback_data="main")
    ]
]

choice_remind: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="➕", callback_data="add"),
        InlineKeyboardButton(text="➖", callback_data="remove"),
        InlineKeyboardButton(text="✏️", callback_data="change"),
        InlineKeyboardButton(text="🙅‍♂️", callback_data="main"),
    ]
]


main_menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
cancel = InlineKeyboardMarkup(inline_keyboard=cancel_button)
confirm = InlineKeyboardMarkup(inline_keyboard=confirm_button)
remind_button = InlineKeyboardMarkup(inline_keyboard=choice_remind)
