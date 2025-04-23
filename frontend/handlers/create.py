from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode

from api.create import request_create_habit
from keyboards.keyboard import cancel, main_menu
from loader import (
    success_save,
    create_title,
    create_body,
    create_number_of_days
)
from states.add import AddState
from handlers.decorator_handlers import decorator_errors

add: Router = Router()


@add.callback_query(F.data == "create")
async def input_name_habits(call: CallbackQuery, state: FSMContext) -> None:
    """The handler asks the user for the name of the habit."""
    await state.set_state(AddState.title)
    await call.message.edit_text(
        text=create_title, parse_mode="HTML", reply_markup=cancel
    )


@add.message(AddState.title)
async def input_describe_habits(mess: Message, state: FSMContext) -> None:
    """The handler asks the user for a description of the habit."""
    await state.update_data(title=mess.text)
    await state.set_state(AddState.describe)
    await mess.answer(
        text=create_body,
        parse_mode=ParseMode.HTML,
        reply_markup=cancel
    )


@add.message(AddState.describe)
async def input_numbers_days(mess: Message, state: FSMContext) -> None:
    """The handler asks the user for the number of days to track."""
    await state.update_data(body=mess.text)
    await state.set_state(AddState.numbers_of_days)
    await mess.answer(
        text=create_number_of_days,
        reply_markup=cancel,
        parse_mode="HTML"
    )


@add.message(AddState.numbers_of_days, F.text.isdigit())
@decorator_errors
async def create_and_record_db(mess: Message, state: FSMContext) -> None:
    """The handler sends all the entered data for saving.."""
    await state.update_data(number_of_days=mess.text)
    await request_create_habit(await state.get_data(), mess.from_user.id)
    await mess.answer(text=success_save, reply_markup=main_menu)
    await state.clear()
