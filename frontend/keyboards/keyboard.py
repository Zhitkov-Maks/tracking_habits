from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu_bot: List[List[InlineKeyboardButton]] = [
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
                text="Открыть архив",
                callback_data="show_archive"
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
