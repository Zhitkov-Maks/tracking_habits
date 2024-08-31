import asyncio
import logging
from pprint import pprint as pp

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Sticker

from config import BOT_TOKEN
from frontend.handlers.login import login_route
from frontend.handlers.registration import register_route
from keyboards.keyboard import main_menu
from loader import greeting, guide
from handlers.addHandler import add


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(add)
dp.include_router(register_route)
dp.include_router(login_route)



@dp.message(CommandStart())
async def greeting_handler(message: types.Message):
    await bot.send_sticker(
        message.chat.id,
        sticker='CAACAgIAAxkBAAMeZsjqmWI_'
                'G7V8iBgvNbq7eZadeJYAAjQBAAJSiZEjE83Xb_UcB1g1BA'
    )
    await message.answer(text=greeting, reply_markup=main_menu)


@dp.callback_query(F.data == "main")
async def _main(
        call: CallbackQuery,
        state: FSMContext
) -> None:
    await state.clear()
    await call.message.answer(text="Меню", reply_markup=main_menu)


@dp.message(F.text == "/help")
async def handler_help(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(guide, reply_markup=main_menu)


@dp.callback_query(F.data == "show")
async def begin_work(callback: CallbackQuery):
    """Обработчик для команды can"""
    await callback.message.answer("fff")
    await callback.message.answer("Меню.", reply_markup=main_menu)


# @dp.message()
# async def test_handler(sticker: Sticker):
#     pp(sticker)
#     await bot.send_sticker(
#         918071512,
#         sticker="CAACAgIAAxkBAAO6ZsuJCQ946lgVJaM12eR3b4zQ4xIAAkcAA1KJkSPYC53LTQJHDTUE")


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
