import asyncio
import logging

from aiogram import Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from config import WORKER_BOT
from handlers.archive import arch
from handlers.create import add
from handlers.detail import detail
from handlers.edit import edit_rout
from handlers.invalid_handler import invalid_router
from handlers.login import auth
from handlers.registration import register_route
from handlers.remind import remind
from handlers.reset_password import reset
from handlers.tracking import track
from handlers.comments import comment_router
from keyboards.keyboard import main_menu
from loader import greeting, guide, menu_bot, options
from utils.common import append_to_session
from utils.remind import create_scheduler_all, add_scheduler_remove_message

dp = Dispatcher()
dp.include_router(add)
dp.include_router(register_route)
dp.include_router(auth)
dp.include_router(detail)
dp.include_router(edit_rout)
dp.include_router(track)
dp.include_router(arch)
dp.include_router(remind)
dp.include_router(reset)
dp.include_router(comment_router)
dp.include_router(invalid_router)


@dp.message(CommandStart())
async def greeting_handler(message: types.Message) -> None:
    """Welcome Handler."""
    # await append_to_session(message.from_user.id, [message])
    await message.answer(
        text=greeting, reply_markup=main_menu, parse_mode="HTML"
    )


@dp.callback_query(F.data == "main")
async def handler_main_button(call: CallbackQuery, state: FSMContext) -> None:
    """Show base bot's menu."""
    await state.clear()
    send_message = await call.message.answer(
        text=menu_bot,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await append_to_session(call.from_user.id, [call, send_message])


@dp.message(F.text == "/main")
async def handler_main_command(message: Message, state: FSMContext) -> None:
    """Show base bot's menu."""
    await state.clear()
    send_message = await message.answer(
        text=menu_bot,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await append_to_session(message.from_user.id, [message, send_message])


@dp.message(F.text == "/guide")
async def handler_help(mess: Message, state: FSMContext) -> None:
    """Shows detailed information about the work of the bot."""
    await state.clear()
    send_message = await mess.answer(
        text=guide, reply_markup=main_menu
    )
    await append_to_session(mess.from_user.id, [mess, send_message])


@dp.callback_query(F.data == "show_commands")
async def show_all_commands(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Shows which commands are still available.
    """
    send_message = await callback.message.edit_text(
        text=options,
        replay_markup=main_menu
    )
    await append_to_session(
        callback.from_user.id, [callback, send_message]
    )


async def main():
    """
    The function launches the bot and also launches the notification
    scheduler to launch notifications for users who have
    there are notification settings.
    """
    await create_scheduler_all()
    await add_scheduler_remove_message()
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(WORKER_BOT)


if __name__ == "__main__":
    asyncio.run(main())
