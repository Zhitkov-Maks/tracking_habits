from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard import main_menu

invalid_router = Router()


@invalid_router.message(F.text)
async def invalid_message_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Ошибка ввода. Будьте внимательнее и попробуйте сначала.",
        reply_markup=main_menu
    )


@invalid_router.callback_query(F.data)
async def invalid_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer(text="I can't show you anything. Sorry!")
