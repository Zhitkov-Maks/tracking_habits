import asyncio
from aiogram.exceptions import TelegramBadRequest
from pathlib import Path
from functools import wraps
from http.client import HTTPException
from typing import Any, Callable, Coroutine, TypeVar
from random import choice

from aiogram.types import (
    Message,
    InlineKeyboardMarkup
)
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery as CQ

from keyboards.keyboard import main_menu
from loader import not_auth
from config import jwt_token_data, WORKER_BOT
from api.get_habit import get_full_info
from utils.habits import generate_message_answer
from keyboards.detail import gen_habit_keyboard
from states.add import HabitState
from stickers.sticker import STICKER_PACK_NOT_DONE, STICKER_PACK_DONE


T = TypeVar("T")


async def remove_message_after_delay(delay: int, message: Message):
    """
    Deleting important user data with a delay.

    :param delay: Delay by seconds.
    :param message: Message for removing.
    :return: None.
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


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
            await WORKER_BOT.send_sticker(
                chat_id=arg.from_user.id,
                sticker=choice(STICKER_PACK_NOT_DONE)
            )

            await WORKER_BOT.send_message(
                arg.from_user.id,
                not_auth,
                parse_mode="HTML",
                reply_markup=main_menu
            )

        except (HTTPException, TelegramBadRequest) as err:
            await WORKER_BOT.send_message(
                arg.from_user.id,
                text=hbold("У нас проблемы с синтернетом 💻🌐!\n"),
                reply_markup=main_menu
            )

        except Exception as err:
            await WORKER_BOT.send_message(
                arg.from_user.id, text=str(err), reply_markup=main_menu
            )

    return wrapper


async def delete_jwt_token(user_id: int) -> None:
    """
    Deletes the jwt token to log out

    :param user_id: ID user.
    """
    try:
        del jwt_token_data[user_id]
    except KeyError:
        pass


async def send_sticker(user_id: int, sticker: str) -> None:
    """
    Sends a random sticker to the user.

    :param user_id: User ID.
    :param sticker: The name of the sticker.
    """
    await WORKER_BOT.send_sticker(chat_id=user_id, sticker=sticker)


async def bot_send_message(state: FSMContext, user_id: int):
    """
    Opens the latest information about the habit.

    :param user_id: User ID.
    :param state: FSMContext for getting data about a habit.
    """
    data: dict = await state.get_data()
    id_: int = data.get("id")
    response: dict = await get_full_info(id_, user_id)
    text: str = await generate_message_answer(response)
    keyboard: InlineKeyboardMarkup = await gen_habit_keyboard()

    await state.set_state(HabitState.action)
    await WORKER_BOT.send_message(
        chat_id=user_id,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

async def choice_sticker(user: int, action: str) -> None:
    """
    Show the sticker depending on the user's choice.
    
    :param user: ID user.
    :param action: Done or not done.
    """
    if action == "done":
        sticker = choice(STICKER_PACK_DONE)
    else:
        sticker = choice(STICKER_PACK_NOT_DONE)
    await send_sticker(user, sticker)