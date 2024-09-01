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
        text="Регистрация",
        callback_data="registration"
    ),
    InlineKeyboardButton(
            text="Вход",
            callback_data="login"
        )
    ],
]

cancel_button = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

main_menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
cancel = InlineKeyboardMarkup(inline_keyboard=cancel_button)
