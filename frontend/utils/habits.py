from datetime import datetime as dt, UTC, datetime, timedelta
from typing import List, Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hitalic
from asyncpg.pgproto.pgproto import timedelta


weekdays: tuple = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс",)
days_ago: Dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
}


async def get_choice_date(call_data: str) -> str:
    """
    Получает дату за некоторый промежуток времени(До 7 дней).
    :param call_data: Число на сколько днй назад нужно получить дату.
    :return str: Дату в виде строки.
    """
    now: datetime.date = dt.now(UTC).date()
    date: datetime = now - timedelta(days=days_ago.get(call_data))
    return str(date)


async def inline_done_not_done() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для добавления отметки о выполнении или невыполнении.
    :return InlineKeyboardMarkup: Возвращает клавиатуру.
    """
    choice: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="✅", callback_data="done"
            ),
            InlineKeyboardButton(
                text="❌", callback_data="not_done"
            ),
            InlineKeyboardButton(
                text="Отмена", callback_data="main"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=choice)


async def get_weekdays() -> dict:
    """
    Получает дату и день недели для добавления отметки о
    выполнении/невыполнении.
    :return dict: Словарь, где ключ количество дней назад,
        а значение кортеж с датой и днем недели.
    """
    today: datetime.date = dt.now().date()
    days = {}
    for i in range(7):
        curr_date = today - timedelta(days=i)
        days.update({i: (
            f"{str(curr_date)[8:10]}.{str(curr_date)[5:7]}",
            weekdays[curr_date.weekday()]
        )})
    return days



async def inline_choice_calendar() -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру с датами для отметки о выполнении/невыполнении.
    :return InlineKeyboardMarkup: Клавиатуру с датами.
    """
    days: dict = await get_weekdays()
    inline_choice = [
        [
            InlineKeyboardButton(
                text=str(days[0][0]) + f"({days[0][1]})",
                callback_data="zero"
            ),
            InlineKeyboardButton(
                text=str(days[1][0]) + f"({days[1][1]})",
                callback_data="one"
            ),
            InlineKeyboardButton(
                text=str(days[2][0]) + f"({days[2][1]})",
                callback_data="two"
            ),
            InlineKeyboardButton(
                text=str(days[3][0]) + f"({days[3][1]})",
                callback_data="three"
            ),
        ],
        [
            InlineKeyboardButton(
                text=str(days[4][0]) + f"({days[4][1]})",
                callback_data="four"
            ),
            InlineKeyboardButton(
                text=str(days[5][0]) + f"({days[5][1]})",
                callback_data="five"
            ),
            InlineKeyboardButton(
                text=str(days[6][0]) + f"({days[6][1]})",
                callback_data="six"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_choice)


async def gen_habit_keyword() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру для действия
    по конкретной привычке.
    :return InlineKeyboardMarkup: Клавиатуру для выбора действий.
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


async def generate_inline_habits_list(
    habits_list: list
) -> InlineKeyboardMarkup:
    """
    Функция для создания списка активных привычек в виде инлайн клавиатуры.
    :param habits_list: Список привычек.
    :return InlineKeyboardMarkup: Инлайн клавиатура со списком привычек.
    """
    inline_habits: List[List[InlineKeyboardButton]] = []
    for obj_habits in habits_list:
        inline_habits.append([
            InlineKeyboardButton(
                text=obj_habits.get("title"),
                callback_data=str(obj_habits.get("id"))
            )
        ])
    inline_habits.append(
        [
            InlineKeyboardButton(
                text="Показать меню",
                callback_data="main"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_habits)


async def count_days_by_date(data: dict) -> tuple:
    """
    Формирует данные об успешных/не успешных днях,
    и сколько дней осталось отслеживать.
    :param data: Дынные для формирования ответа.
    :return tuple: Кортеж с тремя числами.
    """
    end_date: datetime.date = dt.strptime(
        data.get("end_date")[:10], '%Y-%m-%d'
    ).date()
    curr_date: datetime.date = dt.now().date()

    count_done: int = data.get("tracking").get("done")
    count_not_done: int = data.get("tracking").get("not_done")
    days_left: int = (end_date - curr_date).days
    return count_done, count_not_done, days_left


async def generate_message_seven_days(data: list) -> str:
    """
    Генерирует отчет об отслеживании за последние семь дней.
    :param data: Данные об отслеживании.
    :return str: Строку с информацией об отслеживании.
    """
    mess: str = f"{40 * '-'}\n"
    for item in data:
        mess += (f"|   Дата: {hbold(item.get('date')[:10])} - "
                 f"{'✅' if item.get('done') else '❌'}   |\n")
        mess += f"{40 * '-'}\n"
    return mess


async def generate_message_answer(data: dict) -> str:
    """
    Функция генерирует сообщения для показа
    пользователю его конкретной активной/неактивной привычки.
    :param data: Полные данные о привычке и ее отслеживании.
    :return str:  Возвращает строку с подробной информацией.
    """
    count_days: tuple = await count_days_by_date(data)
    report_sevent_days: str = await generate_message_seven_days(
        data.get('tracking').get('all')
    )
    return (
        f"{hbold(data.get("title"))}\n"
        f"{70*'-'}\n"
        f"{hitalic(data.get("body"))}\n"
        f"Дней отслеживать: {hbold(data.get("number_of_days"))}\n"
        f"Дата начала: {hbold(data.get("start_date")[:10])}\n"
        f"Дата окончания: {hbold(data.get("end_date")[:10])}\n"
        f"Успешных дней: {hbold(count_days[0])}\n"
        f"Не успешных дней: {hbold(count_days[1])}\n"
        f"{hbold('Отметки за последние 7 дней:')}\n"
        f"{report_sevent_days}"
        f"Осталось дней: {hbold(count_days[2])} "
        f"дней.\n"
        f"{hbold('Привычка успешно выполнена и помещена в архив.' )
        if count_days[0] == data.get("number_of_days") else ''}\n"
        f"{hbold('Внимание. У вас уже есть три пометки о невыполнении, '
                 'еще одна отметка - данные об отслеживании обнуляться, и '
                 'вам придется начинать сначала!')
        if count_days[1] == 3 else ''}"
    )


async def gen_message_done_not_done(data: dict) -> str:
    """
    Генерация сообщения на добавление отметки о выполнении/невыполнении.
    :param data: Данные о выполнении/невыполнении.
    :return str: Возвращает сообщение.
    """
    return (f"За дату {hbold(data.get("date"))} была сделана "
    f"отметка о "
    f"{'не' if data.get('done') == 'not_done' else ''} "
    f"выполнении.")
