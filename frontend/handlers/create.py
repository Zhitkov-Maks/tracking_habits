import random

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.create import request_create_habit
from handlers.decorator_handlers import decorator_errors
from keyboards.keyboard import cancel, main_menu
from loader import (
    create_body,
    create_number_of_days,
    create_title,
    success_save
)
from states.add import AddState
from utils.common import append_to_session, send_sticker

add: Router = Router()

STICKERS_LIST = [
    "done.webp",
    "done_1.tgs",
    "done_2.tgs",
    "done_3.tgs",
    "done_4.tgs",
    "done_5.tgs"
]


@add.callback_query(F.data == "create")
async def input_name_habits(call: CallbackQuery, state: FSMContext) -> None:
    """The handler asks the user for the name of the habit."""
    await state.set_state(AddState.title)
    send_message = await call.message.answer(
        text=create_title,
        parse_mode="HTML",
        reply_markup=cancel
    )
    await append_to_session(call.from_user.id, [call, send_message])


@add.message(AddState.title)
async def input_describe_habits(mess: Message, state: FSMContext) -> None:
    """The handler asks the user for a description of the habit."""
    await state.update_data(title=mess.text)
    await state.set_state(AddState.describe)
    send_message = await mess.answer(
        text=create_body,
        parse_mode=ParseMode.HTML,
        reply_markup=cancel
    )
    await append_to_session(mess.from_user.id, [mess, send_message])


@add.message(AddState.describe)
async def input_numbers_days(mess: Message, state: FSMContext) -> None:
    """The handler asks the user for the number of days to track."""
    await state.update_data(body=mess.text)
    await state.set_state(AddState.numbers_of_days)
    send_message = await mess.answer(
        text=create_number_of_days,
        reply_markup=cancel,
        parse_mode="HTML"
    )
    await append_to_session(mess.from_user.id, [mess, send_message])


@add.message(AddState.numbers_of_days, F.text.isdigit())
@decorator_errors
async def create_and_record_db(mess: Message, state: FSMContext) -> None:
    """The handler sends all the entered data for saving.."""
    await state.update_data(number_of_days=mess.text)
    await request_create_habit(await state.get_data(), mess.from_user.id)
    await send_sticker(
        mess.from_user.id,
        random.choice(STICKERS_LIST)
    )
    send_message = await mess.answer(
        text=success_save,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await state.clear()
    await append_to_session(mess.from_user.id, [mess, send_message])
