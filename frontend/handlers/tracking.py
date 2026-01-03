from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold

from api.tracking import (
    habit_tracking_mark,
    habit_tracking_mark_update
)
from keyboards.keyboard import confirm
from states.add import HabitState
from keyboards.tracking import inline_choice_calendar, inline_done_not_done
from utils.common import bot_send_message, decorator_errors

track: Router = Router()


@track.callback_query(HabitState.action, F.data == "mark")
@decorator_errors
async def choice_date(call: CallbackQuery, state: FSMContext) -> None:
    """
    Processes the command about the need to mark the habit,
    gets a keyboard to show possible days to mark.
    """
    keyword: InlineKeyboardMarkup = await inline_choice_calendar(days_ago=0)
    await state.set_state(HabitState.done)
    await state.update_data(days_ago=0)
    await call.message.edit_text(
        text=hbold("Выберите день:"),
        reply_markup=keyword,
        parse_mode="HTML"
    )


@track.callback_query(F.data.in_(["next_day", "prev_day"]))
@decorator_errors
async def choice_date_prev(call: CallbackQuery, state: FSMContext) -> None:
    """
    Processes the command about the need to mark the habit,
    gets a keyboard to show possible days to mark.
    """
    days_ago: int = (await state.get_data()).get("days_ago", 0)
    if call.data == "prev_day":
        days_ago += 1
    else:
        days_ago -= 1
        
    keyword: InlineKeyboardMarkup = await inline_choice_calendar(days_ago)
    await state.set_state(HabitState.done)
    await state.update_data(days_ago=days_ago)
    await call.message.edit_text(
        text=hbold("Выберите день:"),
        reply_markup=keyword,
        parse_mode="HTML"
    )


@track.callback_query(HabitState.done)
@decorator_errors
async def choice_done(call: CallbackQuery, state: FSMContext) -> None:
    """
    The data handler after entering the date of the mark.
    Gets the keyboard to select completed/not completed.
    """
    keyword: InlineKeyboardMarkup = await inline_done_not_done()

    await state.update_data(date=call.data)
    await state.set_state(HabitState.date)
    await call.message.edit_text(
        text=hbold(
            "Выберите:\n"
            "✅ - если выполнили\n"
            "❌ - если не выполнили."),
        reply_markup=keyword,
        parse_mode="HTML"
    )


@track.callback_query(HabitState.date, F.data.in_(["done", "not_done"]))
@decorator_errors
async def mark_tracking_habit_done(
        call: CallbackQuery, state: FSMContext
) -> None:
    """
    Processes the executed/not executed commands.
    Calls the function to save the mark in the database.
    If everything went well,
    it also re-shows the current habit.
    """
    await state.update_data(done=call.data)
    data: dict = await state.get_data()
    status, response = await habit_tracking_mark(data, call.from_user.id)

    if status in (200, 201):
        await bot_send_message(state, call.from_user.id)
    else:
        await state.set_state(HabitState.confirm)
        await call.message.edit_text(
            text=response + "\nХотите изменить запись?",
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
    await bot_send_message(state, call.from_user.id)
