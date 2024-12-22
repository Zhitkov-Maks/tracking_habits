from datetime import datetime as dt, datetime, UTC, timedelta
from typing import Dict

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
    Gets the date for a certain period of time (Up to 7 days).
    :param call_data: The number for how many days ago you need to get the date.
    :return str: The date in the form of a string.
    """
    now: datetime.date = dt.now(UTC).date()
    date: datetime.date = now - timedelta(days=days_ago.get(call_data))
    return str(date)
