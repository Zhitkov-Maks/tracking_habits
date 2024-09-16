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
                text="Регистрация",
                callback_data="registration"
            ),
            InlineKeyboardButton(
                text="Напоминание",
                callback_data="remind"
            )
        ],
        [
            InlineKeyboardButton(
                text="Гайд по работе с ботом",
                callback_data="guide"
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

choice_remind = [
    [
        InlineKeyboardButton(text="Добавить", callback_data="add"),
        InlineKeyboardButton(text="Удалить", callback_data="remove"),
    ],
    [
        InlineKeyboardButton(text="Изменить время", callback_data="change"),
        InlineKeyboardButton(text="Отмена", callback_data="main"),

    ]
]


main_menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
cancel = InlineKeyboardMarkup(inline_keyboard=cancel_button)
confirm = InlineKeyboardMarkup(inline_keyboard=confirm_button)
remind_button = InlineKeyboardMarkup(inline_keyboard=choice_remind)
