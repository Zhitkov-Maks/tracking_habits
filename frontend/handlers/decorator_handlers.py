from pathlib import Path
from functools import wraps
from http.client import HTTPException
from typing import Any, Callable, Coroutine, TypeVar

from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery as CQ
from aiogram.types import Message
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
            sticker_path = Path(__file__).parent.parent.joinpath(
                "stickers", "stop_not_auth.tgs"
            )
            input_file = FSInputFile(sticker_path)
            sticker = await WORKER_BOT.send_sticker(
                chat_id=arg.from_user.id,
                sticker=input_file
            )
            send_message = await WORKER_BOT.send_message(
                arg.from_user.id,
                not_auth,
                parse_mode="HTML",
                reply_markup=main_menu
            )
            await append_to_session(arg.from_user.id, [send_message, sticker])

        except HTTPException as err:
            send_message = await WORKER_BOT.send_message(
                arg.from_user.id, text=str(err), reply_markup=main_menu
            )
            await append_to_session(arg.from_user.id, [send_message])

    return wrapper
