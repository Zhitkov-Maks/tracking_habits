from datetime import datetime as dt, UTC, datetime, timedelta
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hitalic
from asyncpg.pgproto.pgproto import timedelta


weekdays = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс",)
days_ago = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
}


async def get_choice_date(call_data: str) -> str:
    now: datetime.date = dt.now(UTC).date()
    date: datetime = now - timedelta(days=days_ago.get(call_data))
    return str(date)


async def inline_done_not_done() -> InlineKeyboardMarkup:
    choice = [
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


async def gen_habit_keyword():
    """
    Функция генерирует клавиатуру для действия
    по конкретной привычке.
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
                text="Убрать все отметки",
                callback_data="clean"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_actions)


async def generate_inline_habits_list(
    habits_list: list
) -> InlineKeyboardMarkup:
    """
    Функция для создания списка активных привычек в виде инлайн клавиатуры.
    """
    inline_habits: list = []
    for obj_habits in habits_list:
        inline_habits.append([
            InlineKeyboardButton(
                text=obj_habits.get("title"),
                callback_data=str(obj_habits.get("id"))
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_habits)


async def count_days_by_date(data: dict) -> tuple:
    end_date: datetime.date = dt.strptime(
        data.get("end_date")[:10], '%Y-%m-%d'
    ).date()
    curr_date: datetime.date = dt.now().date()

    count_done: int = len(data.get("tracking").get("done"))
    count_not_done: int = len(data.get("tracking").get("not_done"))
    days_left: datetime.day = (end_date - curr_date).days - 1
    return count_done, count_not_done, days_left


async def generate_message_seven_days(data: list) -> str:
    mess = f"{30 * '-'}\n"
    for item in data:
        mess += (f"Дата: {hbold(item.get('date')[:10])} "
                 f"{'✅' if item.get('done') else '❌'}\n")
        mess += f"{30 * '-'}\n"
    return mess


async def generate_message_answer(data: dict) -> str:
    """
    Функция генерирует сообщения для показа
    пользователю его конкретной активной привычки.
    """
    count_days: tuple = await count_days_by_date(data)
    report_sevent_days: str = await generate_message_seven_days(
        data.get('tracking').get('all')
    )
    text = (
        f"{hbold(data.get("title"))}\n"
        f"{70*'-'}\n"
        f"{hitalic(data.get("body"))}\n"
        f"Дней отслеживать: {hbold(data.get("number_of_days"))}\n"
        f"Дата начала: {hbold(data.get("start_date")[:10])}\n"
        f"Успешных дней: {hbold(count_days[0])}\n"
        f"Не успешных дней: {hbold(count_days[1])}\n"
        f"{hbold('Последние отмеченные дни:')}\n"
        f"{report_sevent_days}"
        f"Осталось дней: {hbold(count_days[2])} дней."
    )
    return text


async def gen_message_done_not_done(data: dict) -> str:
    return (f"За дату {hbold(data.get("date"))} была сделана "
    f"отметка о "
    f"{'не' if data.get('done') == 'not_done' else ''} "
    f"выполнении.")
