import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN
from handlers.remind import remind
from handlers.archive import arch
from handlers.edit import edit_rout
from handlers.detail import detail
from handlers.login import auth
from handlers.registration import register_route
from handlers.tracking import track
from utils.remind import create_scheduler_all
from keyboards.keyboard import main_menu
from loader import greeting, guide
from handlers.create import add


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(add)
dp.include_router(register_route)
dp.include_router(auth)
dp.include_router(detail)
dp.include_router(edit_rout)
dp.include_router(track)
dp.include_router(arch)
dp.include_router(remind)


@dp.message(CommandStart())
async def greeting_handler(message: types.Message) -> None:
    """Welcome Handler."""
    await message.answer(text=greeting, reply_markup=main_menu)


@dp.callback_query(F.data == "main")
async def handler_main(call: CallbackQuery, state: FSMContext) -> None:
    """Show base bot's menu."""
    await state.clear()
    await call.message.answer(text="Меню", reply_markup=main_menu)


@dp.message(F.text == "/main")
async def handler_main(message: Message, state: FSMContext) -> None:
    """Show base bot's menu."""
    await state.clear()
    await message.answer(text="Меню", reply_markup=main_menu)


@dp.callback_query(F.data == "guide")
async def handler_help(call: types.CallbackQuery, state: FSMContext) -> None:
    """Shows detailed information about the work of the bot."""
    await state.clear()
    await call.message.answer(text=guide, reply_markup=main_menu)


async def main():
    """
    The function launches the bot and also launches the notification
    scheduler to launch notifications for users who have
    there are notification settings.
    """
    await create_scheduler_all()
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
