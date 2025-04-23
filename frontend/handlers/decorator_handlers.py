from functools import wraps
from typing import TypeVar, ParamSpec, Callable
from http.client import HTTPException

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN
from keyboards.keyboard import main_menu
from loader import not_auth

bot = Bot(token=BOT_TOKEN)


T = TypeVar("T")
P = ParamSpec("P")


def decorator_errors(func: Callable[P, T]) -> Callable[P, T]:
    """
    A decorator for the callback and message processing function.
    """
    @wraps(func)
    async def wrapper(arg: P, state: FSMContext) -> None:
        """
        Wrapper for error handling when executing a function
        """
        try:
            await func(arg, state)

        except KeyError:
            await bot.send_message(
                arg.from_user.id, not_auth, reply_markup=main_menu
            )

        except HTTPException as err:
            await bot.send_message(
                arg.from_user.id, text=str(err), reply_markup=main_menu
            )
    return wrapper
