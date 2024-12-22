import asyncio

from aiogram.types import Message


async def remove_message_after_delay(delay: int, message: Message):
    """
    Deleting important user data with a delay.

    :param delay: Delay by seconds.
    :param message: Message for removing.
    :return: None.
    """
    await asyncio.sleep(delay)
    await message.delete()
