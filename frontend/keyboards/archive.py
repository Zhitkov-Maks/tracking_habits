from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_inline_habits_list(
        habits_list: List[Dict[str, str | int]]
) -> InlineKeyboardMarkup:
    """
    A function for creating a list of active habits in the form
    of an inline keyboard.
    :param habits_list: List of habits from the archive.
    :return InlineKeyboardMarkup: An inline keyboard with a list of habits.
    """
    inline_habits: List[List[InlineKeyboardButton]] = []
    for obj_habits in habits_list:
        inline_habits.append([
            InlineKeyboardButton(
                text=obj_habits.get("title"),
                callback_data=str(obj_habits.get("id"))
            )
        ])
    inline_habits.append([
            InlineKeyboardButton(
                text="Показать меню",
                callback_data="main"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_habits)


async def gen_habit_keyword_archive():
    """
    The function generates a keyboard for the action
    according to a specific habit in the archive.
    :return InlineKeyboardButton: A keyboard with a choice of actions.
    """
    inline_actions: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="Удалить",
                callback_data="delete"
            ),
            InlineKeyboardButton(
                text="Востан-ть",
                callback_data="un_archive"
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)
