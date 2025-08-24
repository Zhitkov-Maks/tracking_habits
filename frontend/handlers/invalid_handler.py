from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.keyboard import main_menu
from utils.common import append_to_session, decorator_errors

invalid_router = Router()


@invalid_router.message(F.text)
@decorator_errors
async def invalid_message_text(message: Message, state: FSMContext):
    await state.clear()
    send_message = await message.answer(
        text="Ошибка ввода. Будьте внимательнее и попробуйте сначала.",
        reply_markup=main_menu
    )
    await append_to_session(message.from_user.id, [message, send_message])


@invalid_router.callback_query(F.data)
@decorator_errors
async def invalid_callback(callback: CallbackQuery) -> None:
    send_message = await callback.answer(
        text="I can't show you anything. Sorry!"
    )
    await append_to_session(callback.from_user.id, [callback, send_message])
