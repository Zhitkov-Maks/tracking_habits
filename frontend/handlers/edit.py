from typing import Dict

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram import F

from api.edit import request_update_habit
from api.get_habit import get_full_info
from handlers.decorator_handlers import decorator_errors
from keyboards.detail import gen_habit_keyword
from keyboards.edit import generate_inline_choice_edit
from keyboards.keyboard import cancel, confirm
from loader import update_data
from states.edit import FullEditState, PartialEditHabit
from states.add import HabitState
from utils.habits import generate_message_answer

edit_rout = Router()


@edit_rout.callback_query(HabitState.action, F.data == "edit")
async def choosing_upgrade_option(call: CallbackQuery) -> None:
    """Handler for selecting a habit change option."""
    await call.message.answer(
        text="Выберите что вы хотите изменить.",
        reply_markup=await generate_inline_choice_edit()
    )


@edit_rout.callback_query(F.data == "edit_title")
async def update_title(callback: CallbackQuery, state: FSMContext) -> None:
    """Handler for entering a new habit name."""
    await state.set_state(PartialEditHabit.title)
    text: str = hbold("Введите новое название для привычки.")
    await callback.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@edit_rout.message(PartialEditHabit.title)
async def partial_update_title(message: Message, state: FSMContext) -> None:
    """
    The handler saves the new habit name and requests approval to save it.
    """
    await state.update_data(title=message.text)
    await state.set_state(PartialEditHabit.save)
    await message.answer(
        hbold("Сохранить новое название привычки?"),
        parse_mode="HTML",
        reply_markup=confirm
    )


@edit_rout.callback_query(F.data == "edit_body")
async def update_body(callback: CallbackQuery, state: FSMContext) -> None:
    """Handler for entering a new habit description."""
    await state.set_state(PartialEditHabit.body)
    text: str = hbold("Введите новое описание для привычки.")
    await callback.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@edit_rout.message(PartialEditHabit.body)
async def partial_update_body(message: Message, state: FSMContext) -> None:
    """
    The handler saves the new habit description and requests
    approval to save it.
    """
    await state.update_data(body=message.text)
    await state.set_state(PartialEditHabit.save)
    await message.answer(
        hbold("Сохранить новое описание для привычки?"),
        parse_mode="HTML",
        reply_markup=confirm
    )


@edit_rout.callback_query(F.data == "edit_period")
async def update_period(callback: CallbackQuery, state: FSMContext) -> None:
    """Handler for entering a new habit numbers_of_days."""
    await state.set_state(PartialEditHabit.number_of_days)
    text: str = hbold("Введите новое количество дней для отслеживания "
                      "привычки.")
    await callback.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@edit_rout.message(PartialEditHabit.number_of_days)
async def partial_update_body(message: Message, state: FSMContext) -> None:
    """
    The handler saves the new habit numbers_of_days and requests
    approval to save it.
    """
    await state.update_data(number_of_days=message.text)
    await state.set_state(PartialEditHabit.save)
    await message.answer(
        hbold("Сохранить количество дней для отслеживания привычки?"),
        parse_mode="HTML",
        reply_markup=confirm
    )


@edit_rout.callback_query(PartialEditHabit.save, F.data == "yes")
@decorator_errors
async def partial_update_save(callback: CallbackQuery, state: FSMContext) -> None:
    """
    The handler saves new data for the habit, displays a notification
    of successful saving, and opens the habit with updated data.
    """
    data: Dict[str, str | int] = await state.get_data()
    await request_update_habit(data, callback.from_user.id)
    await callback.answer(update_data, show_alert=True)

    response: dict = await get_full_info(data.get("id"), callback.from_user.id)
    text: str = await generate_message_answer(response)
    await callback.message.answer(
        text=text, parse_mode="HTML", reply_markup=await gen_habit_keyword()
    )


@edit_rout.callback_query(F.data == "edit_full")
async def full_edit_habit_title(call: CallbackQuery, state: FSMContext) -> None:
    """Entering a new habit name when editing a habit."""
    await state.set_state(FullEditState.title)
    text = hbold("1-й этап") + ("\nДайте название привычке которую вы "
                                "хотите отслеживать: ")
    await call.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@edit_rout.message(FullEditState.title)
async def full_edit_description_habit(mess: Message, state: FSMContext) -> None:
    """Entering a new description of a habit when editing a habit."""
    await state.update_data(title=mess.text)
    await state.set_state(FullEditState.describe)
    await mess.answer(
        text=hbold("2-й этап") + "\nВведите новое описание привычки :",
        parse_mode=ParseMode.HTML,
        reply_markup=cancel
    )


@edit_rout.message(FullEditState.describe)
async def full_edit_habit_number_of_days(mess: Message,state: FSMContext) -> None:
    """Entering a new number of days to track a habit."""
    await state.update_data(body=mess.text)
    await state.set_state(FullEditState.numbers_of_days)
    await mess.answer(
        text=hbold("3-й этап\n") + "Сколько дней будем отслеживать?",
        reply_markup=cancel
    )


@edit_rout.message(FullEditState.numbers_of_days, F.text.isdigit())
@decorator_errors
async def full_create_and_record_db(mess: Message,state: FSMContext) -> None:
    """Saving an updated habit."""
    await state.update_data(number_of_days=mess.text)
    data: Dict[str, int] = await state.get_data()
    await request_update_habit(data, mess.from_user.id)
    await mess.answer(text=update_data)

    # Открываем привычку с обновленными данными.
    response: dict = await get_full_info(data.get("id"), mess.from_user.id)
    text: str = await generate_message_answer(response)
    await mess.answer(
        text=text, parse_mode="HTML", reply_markup=await gen_habit_keyword()
    )
