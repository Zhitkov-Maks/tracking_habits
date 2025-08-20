from datetime import date
from typing import Dict, List, Tuple

from aiogram.utils.markdown import hbold, hitalic
from loader import to_archive, warning

month_dict: Dict[int, str] = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря"
}


async def count_days_by_date(
        data: Dict[str, dict]
) -> Tuple[int, int, int]:
    """
    Generates data about successful/unsuccessful days,
    and how many days are left to track.
    :param data: Data for forming the response.
    :return tuple: A tuple with three numbers.
    """
    all_days: date = data.get("number_of_days")

    count_done: int = data.get("tracking", {}).get("done", 0)
    count_not_done: int = data.get("tracking", {}).get("not_done", 0)
    days_left: int = all_days - count_done
    return count_done, count_not_done, days_left


async def generate_message_seven_days(data: List[Dict[str, str]]) -> str:
    """
    Generates a tracking report for the last seven days.
    :param data: Tracking data.
    :return str: A line with tracking information.
    """
    mess = f"{40 * "-"}\n"
    for item in data:
        date: int = int(item.get('date', "")[5:7])
        mess += (
            f"|   Дата: "
            f"{hbold(item.get('date', "")[8:10])} {month_dict.get(date)} - "
            f"{'✅' if item.get('done') else '❌'}   |\n")
        mess += f"{40 * "-"}\n"
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
        data.get('tracking', {}).get('all')
    )
    return (
        f"{hbold(data.get("title"))}\n\n"
        f"{hitalic(data.get("body"))}\n\n"
        f"Дней отслеживать: {hbold(data.get("number_of_days"))};\n"
        f"Дата начала: {hbold(data.get("start_date", "")[:10])};\n"
        f"Дата окончания: {hbold(data.get("end_date", "")[:10])};\n"
        f"Успешных дней: {hbold(count_days[0])};\n"
        f"Не успешных дней: {hbold(count_days[1])};\n"

        f"{hbold("\nОтметки за последние 7 дней:") if len(
            data.get("tracking", "").get("all")) > 0 else
            hbold("\nОтметки за последние 7 дней отсутствуют.")}\n"

        f"{report_sevent_days}"
        f"Осталось дней: {hbold(count_days[2])}.\n"

        f"{hbold(to_archive) if (
            count_days[0] == data.get("number_of_days")
        ) else ''}\n"

        f"{hbold(warning) if count_days[1] == 3 else ''}"
    )


async def get_base_data_habit(
        data: Dict[str, str | int]
) -> Tuple[str, str, int]:
    """
    Returns a tuple of basic habit data.
    :param data: Habit Data
    :return: A tuple with three data.
    """
    title: str = data.get("title", "")
    body: str = data.get("body", "")
    numbers_of_days: int = data.get("number_of_days", 0)
    return title, body, numbers_of_days
