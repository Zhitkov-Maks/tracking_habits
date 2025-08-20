import asyncio
from aiogram.exceptions import TelegramBadRequest
from pathlib import Path

from aiogram.types import Message, CallbackQuery, FSInputFile
from config import user_sessions, jwt_token_data, WORKER_BOT


async def remove_message_after_delay(delay: int, message: Message):
    """
    Deleting important user data with a delay.

    :param delay: Delay by seconds.
    :param message: Message for removing.
    :return: None.
    """
    await asyncio.sleep(delay)
    await message.delete()


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
    sticker_path = Path(__file__).parent.parent.joinpath(
        "stickers", sticker
    )
    input_file = FSInputFile(sticker_path)
    sticker: Message = await WORKER_BOT.send_sticker(
        chat_id=user_id,
        sticker=input_file
    )
    asyncio.create_task(remove_message_after_delay(7, sticker))
