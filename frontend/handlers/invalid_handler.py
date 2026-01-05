from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram.enums import ContentType

from keyboards.keyboard import main_menu
from config import WORKER_BOT

invalid_router = Router()


@invalid_router.message(F.text)
async def invalid_message_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Ошибка ввода. Будьте внимательнее и попробуйте сначала.",
        reply_markup=main_menu
    )


@invalid_router.callback_query(F.data)
async def invalid_callback(callback: CallbackQuery) -> None:
    await callback.answer(
        text="I can't show you anything. Sorry!"
    )


@invalid_router.message(F.content_type == ContentType.STICKER)
async def handle_sticker(message: Message):
    sticker = message.sticker
    sticker_id = sticker.file_id
    await message.answer(
        text=sticker_id
    )
    await WORKER_BOT.send_sticker(
        chat_id=message.chat.id,
        sticker=sticker_id
    )
