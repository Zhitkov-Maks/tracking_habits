from datetime import datetime as dt, datetime
from typing import Dict, List, Tuple

from aiogram.utils.markdown import hbold, hitalic


async def count_days_by_date(
        data: Dict[str, str | dict]
) -> Tuple[int, int, int]:
    """
    Generates data about successful/unsuccessful days,
    and how many days are left to track.
    :param data: Data for forming the response.
    :return tuple: A tuple with three numbers.
    """
    end_date: datetime.date = dt.strptime(
        data.get("end_date")[:10], '%Y-%m-%d'
    ).date()
    curr_date: datetime.date = dt.now().date()

    count_done: int = data.get("tracking").get("done")
    count_not_done: int = data.get("tracking").get("not_done")
    days_left: int = (end_date - curr_date).days
    return count_done, count_not_done, days_left


async def generate_message_seven_days(data: List[Dict[str, str]]) -> str:
    """
    Generates a tracking report for the last seven days.
    :param data: Tracking data.
    :return str: A line with tracking information.
    """
    mess: str = f"{40 * '-'}\n"
    for item in data:
        mess += (f"|   Дата: {hbold(item.get('date')[:10])} - "
                 f"{'✅' if item.get('done') else '❌'}   |\n")
        mess += f"{40 * '-'}\n"
    return mess


async def generate_message_answer(data: dict) -> str:
    """
    The function generates messages to show
    the user his specific active/inactive habit.
    :param data: Complete data about the habit and its tracking.
    :return str: Returns a string with detailed information.
    """
    count_days: Tuple[int, int, int] = await count_days_by_date(data)
    report_sevent_days: str = await generate_message_seven_days(
        data.get('tracking').get('all')
    )
    return (
        f"{hbold(data.get("title"))}\n"
        f"{70*'-'}\n"
        f"{hitalic(data.get("body"))}\n"
        f"{70*'-'}\n"
        f"Дней отслеживать: {hbold(data.get("number_of_days"))}\n"
        f"Дата начала: {hbold(data.get("start_date")[:10])}\n"
        f"Дата окончания: {hbold(data.get("end_date")[:10])}\n"
        f"Успешных дней: {hbold(count_days[0])}\n"
        f"Не успешных дней: {hbold(count_days[1])}\n"
        f"{hbold('Отметки за последние 7 дней:') 
        if len(data.get('tracking').get('all')) > 0 
        else "Отметки за последние 7 дней отсутствуют."}\n"
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
    Generating a message to add a mark of completion/non-completion.
    :param data: Data on completion/non-completion.
    :return str: Returns the message.
    """
    return (f"За дату {hbold(data.get("date"))} была сделана "
    f"отметка о "
    f"{'не' if data.get('done') == 'not_done' else ''} "
    f"выполнении.")


async def get_base_data_habit(
        data: Dict[str, str | int]
) -> Tuple[str, str, int]:
    """
    Returns a tuple of basic habit data.
    :param data: Habit Data
    :return: A tuple with three data.
    """
    title: str = data.get("title")
    body: str = data.get("body")
    numbers_of_days: int = data.get("number_of_days")
    return title, body, numbers_of_days
