from typing import Dict

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from api.get_habit import get_full_info
from api.tracking import (
    habit_tracking_mark,
    habit_tracking_mark_update
)
from handlers.decorator_handlers import decorator_errors
from keyboards.keyboard import confirm
from states.add import HabitState
from utils.habits import generate_message_answer, gen_habit_keyword

from keyboards.tracking import inline_choice_calendar, inline_done_not_done
from utils.tracking import get_choice_date, days_ago

track: Router = Router()


@track.callback_query(HabitState.action, F.data == "mark")
async def choice_date(call: CallbackQuery, state: FSMContext) -> None:
    """
    Processes the command about the need to mark the habit,
    gets a keyboard to show possible days to mark.
    """
    keyword: InlineKeyboardMarkup = await inline_choice_calendar()
    await state.set_state(HabitState.done)
    await call.message.answer(
        text="Выберите дату для отметки о выполнении.", reply_markup=keyword
    )


@track.callback_query(HabitState.done, F.data.in_(days_ago))
async def choice_done(call: CallbackQuery, state: FSMContext) -> None:
    """
    The data handler after entering the date of the mark.
    Gets the keyboard to select completed/not completed.
    """
    date: str = await get_choice_date(call.data)
    keyword: InlineKeyboardMarkup = await inline_done_not_done()

    await state.update_data(date=date)
    await state.set_state(HabitState.date)
    await call.message.answer(
        text="Выберите выполнено/не выполнено", reply_markup=keyword)


@track.callback_query(HabitState.date, F.data.in_(["done", "not_done"]))
@decorator_errors
async def mark_tracking_habit_done(
        call: CallbackQuery, state: FSMContext
) -> None:
    """
    Processes the executed/not executed commands.
    Calls the function to save the mark in the database. If everything went well,
    it also re-shows the current habit.
    """
    await state.update_data(done=call.data)
    data: dict = await state.get_data()
    status, response = await habit_tracking_mark(data, call.from_user.id)

    if status in (200, 201):
        result: Dict[str, str] = \
            await get_full_info(data.get("id"), call.from_user.id)
        await state.set_state(HabitState.action)
        await call.message.answer(
            text=await generate_message_answer(result),
            parse_mode="HTML",
            reply_markup=await gen_habit_keyword()
        )

    else:
        await state.set_state(HabitState.confirm)
        await call.message.answer(
            text=response + f"\nХотите изменить запись?",
            reply_markup=confirm
        )


@track.callback_query(HabitState.confirm, F.data == "yes")
@decorator_errors
async def mark_tracking_habit_update(
        call: CallbackQuery, state: FSMContext
) -> None:
    """Handles overwriting habits."""
    data: dict = await state.get_data()
    await habit_tracking_mark_update(data, call.from_user.id)
    response: dict = await get_full_info(data.get("id"), call.from_user.id)

    await state.set_state(HabitState.action)
    await call.message.answer(
        text=await generate_message_answer(response),
        parse_mode="HTML",
        reply_markup=await gen_habit_keyword()
    )
