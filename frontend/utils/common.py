import asyncio
from aiogram.exceptions import TelegramBadRequest
from pathlib import Path
from functools import wraps
from http.client import HTTPException
from typing import Any, Callable, Coroutine, TypeVar

from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery as CQ

from keyboards.keyboard import main_menu
from loader import not_auth
from config import user_sessions, jwt_token_data, WORKER_BOT
from api.get_habit import get_full_info
from utils.habits import generate_message_answer
from keyboards.detail import gen_habit_keyboard
from states.add import HabitState


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


async def append_to_session(
    user_id: int, messages: list[Message | CallbackQuery]
) -> None:
    """
    A function for adding messages that we will delete when we
    click on the clear button.

    :param user_id: ID user.
    :param messages: A set with messages to delete.
    """
    for mess in messages:
        if isinstance(mess, Message):
            user_sessions[user_id].add((mess.chat.id, mess.message_id))

        if isinstance(mess, CallbackQuery) and mess.message is not None:
            user_sessions[user_id].add(
                (mess.message.chat.id, mess.message.message_id)
            )


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

        except Exception as err:
            send_message = await WORKER_BOT.send_message(
                arg.from_user.id, text=str(err), reply_markup=main_menu
            )
            await append_to_session(arg.from_user.id, [send_message])

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


async def delete_sessions(user_id: int) -> None:
    """
    Deleting chat messages and jwt token.

    :param user_id: ID user.
    """
    messages: set[tuple[int, int]] = user_sessions.get(user_id, set())
    for chat_id, message_id in messages:
        try:
            await WORKER_BOT.delete_message(chat_id, message_id)
        except TelegramBadRequest:
            # Если сообщение вдруг уже удалено.
            pass


async def send_sticker(user_id: int, sticker: str) -> None:
    """
    Sends a random sticker to the user.

    :param user_id: User ID.
    :param sticker: The name of the sticker.
    """
    sticker_path = Path(__file__).parent.parent.joinpath(
        "stickers", sticker
    )
    input_file = FSInputFile(sticker_path)
    sticker: Message = await WORKER_BOT.send_sticker(
        chat_id=user_id,
        sticker=input_file
    )
    asyncio.create_task(remove_message_after_delay(60 * 5, sticker))


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
    send_message = await WORKER_BOT.send_message(
        chat_id=user_id,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await append_to_session(user_id, [send_message])


async def delete_old_messages() -> None:
    """
    Deletes messages for the last 24 hours from all users.
    To avoid taking up memory.
    """
    users: list[int] = list(user_sessions.keys())
    for user_id in users:
        await delete_sessions(user_id)
