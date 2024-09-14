from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu_bot = [
        [
            InlineKeyboardButton(
                text="Добавить привычку",
                callback_data="create"
            ),
             InlineKeyboardButton(
                 text="Показать привычки",
                 callback_data="show_habits"
            )
        ],
        [
            InlineKeyboardButton(
                text="Архив",
                callback_data="show_archive"
            ),
            InlineKeyboardButton(
                text="Авторизация",
                callback_data="login"
            )
        ],
        [
            InlineKeyboardButton(
                text="Инструкция",
                callback_data="instruction"
            ),
            InlineKeyboardButton(
                text="Напоминание",
                callback_data="remind"
            )
        ],
    ]

cancel_button = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

confirm_button = [
    [
        InlineKeyboardButton(text="Да", callback_data="yes"),
        InlineKeyboardButton(text="Нет", callback_data="main")
    ]
]


main_menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
cancel = InlineKeyboardMarkup(inline_keyboard=cancel_button)
confirm = InlineKeyboardMarkup(inline_keyboard=confirm_button)
