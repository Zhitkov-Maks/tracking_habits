from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import PAGE_SIZE


async def generate_inline_habits_list(
        habits_list: List[Dict[str, str | int]], page
) -> InlineKeyboardMarkup:
    """
    A function for creating a list of active habits in the form
    of an inline keyboard.
    :param habits_list: List of habits from the archive.
    :param page: The page you need to display.
    :return InlineKeyboardMarkup: An inline keyboard with a list of habits.
    """
    size: int = len(habits_list) if PAGE_SIZE > len(habits_list) else PAGE_SIZE
    inline_habits: List[List[InlineKeyboardButton]] = []
    for i in range(size):
        inline_habits.append([
            InlineKeyboardButton(
                text=habits_list[i].get("title"),
                callback_data=str(habits_list[i].get("id"))
            )
        ])

    prev_data, text_prev = "None prev", "-"
    next_data, text_next = "None next", "-"

    if page > 1:
        prev_data, text_prev = "prev_page", "<<"

    if PAGE_SIZE < len(habits_list):
        next_data, text_next = "next_page", ">>"

    inline_habits.append([
            InlineKeyboardButton(
                text=text_prev,
                callback_data=prev_data
            ),
            InlineKeyboardButton(
                text="Меню",
                callback_data="main"
            ),
            InlineKeyboardButton(
                text=text_next,
                callback_data=next_data
            ),
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
