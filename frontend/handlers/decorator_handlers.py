from functools import wraps
from typing import Coroutine, TypeVar, Callable, Any
from http.client import HTTPException

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery as CQ

from config import WORKER_BOT
from keyboards.keyboard import main_menu
from loader import not_auth
from utils.common import append_to_session


T = TypeVar("T")


def decorator_errors(
    func: Callable[[Message | CQ, FSMContext], Coroutine[Any, Any, T]]
) -> Callable[[Message | CQ, FSMContext], Coroutine[Any, Any, None]]:
    """
    A decorator for the callback and message processing function.
    """
    @wraps(func)
    async def wrapper(arg: Message | CQ, state: FSMContext) -> None:
        """
        Wrapper for error handling when executing a function
        """
        try:
            await func(arg, state)

        except KeyError:
            send_message = await WORKER_BOT.send_message(
                arg.from_user.id, not_auth, reply_markup=main_menu
            )
            await append_to_session(arg.from_user.id, [send_message])

        except HTTPException as err:
            send_message = await WORKER_BOT.send_message(
                arg.from_user.id, text=str(err), reply_markup=main_menu
            )
            await append_to_session(arg.from_user.id, [send_message])

    return wrapper
