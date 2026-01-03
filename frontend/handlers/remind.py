from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from api.remind import add_time_remind, remove_time
from keyboards.keyboard import (
    remind_button,
    main_menu,
    confirm
)
from keyboards.remind import create_time, actions_list, update_time

from states.remind import RemindState
from utils.remind import (
    add_send_message,
    remove_scheduler_job
)
from utils.common import decorator_errors
from loader import menu_remind, choice_hour, menu_bot

remind: Router = Router()


@remind.callback_query(F.data == "remind")
@decorator_errors
async def start_work_to_remind(call: CallbackQuery, state: FSMContext) -> None:
    """
    A command handler for working with reminders.
    Shows a menu for selecting an action.
    """
    await state.set_state(RemindState.start)
    await call.message.edit_text(
        text=menu_remind,
        reply_markup=remind_button,
        parse_mode="HTML"
    )


@remind.callback_query(RemindState.start, F.data == "remove")
@decorator_errors
async def confirm_to_remove_remind(
        call: CallbackQuery, state: FSMContext
) -> None:
    """
    The handler of the command to delete the reminder.
    Shows the menu for confirmation.
    """
    await state.set_state(RemindState.confirm)
    await call.message.edit_text(
        text="Вы уверены?", reply_markup=confirm
    )


@remind.callback_query(RemindState.confirm, F.data == "yes")
@decorator_errors
async def finalize_remove(call: CallbackQuery, state: FSMContext) -> None:
    """The handler for deleting the reminder."""
    await remove_time(call.from_user.id)
    await remove_scheduler_job(call.from_user.id)
    await call.answer(text="Напоминание удалено", show_alert=True)
    await call.message.edit_text(
        text=menu_bot,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await state.clear()


@remind.callback_query(RemindState.start, F.data.in_(["add", "change"]))
#@decorator_errors
async def add_remind(call: CallbackQuery, state: FSMContext) -> None:
    """
    A handler for adding or changing the reminder time.
    Shows the keyboard to select the hour for notification.
    """
    await state.set_state(RemindState.add)

    if call.data == "change":
        await state.update_data(update=True)

    else:
        await state.update_data(update=False)

    await state.update_data(hours=12, minutes=0)
    await call.message.edit_text(
        text=choice_hour,
        reply_markup=await create_time()
    )


@remind.callback_query(F.data.in_(actions_list))
@decorator_errors
async def update_clock(call: CallbackQuery, state: FSMContext) -> None:
    """
    A handler for adding or changing the reminder time.
    Shows the keyboard to select the hour for notification.
    """
    await state.set_state(RemindState.add)
    await call.message.edit_text(
        text=choice_hour,
        reply_markup=await update_time(call.data, state)
    )


@remind.callback_query(RemindState.add, F.data == "save_time")
#@decorator_errors
async def finalize_add_remind(call: CallbackQuery, state: FSMContext) -> None:
    """The final handler for adding a reminder."""
    data = await state.get_data()
    update: bool = data["update"]
    hours, minutes = data["hours"], data["minutes"]
    add_data: dict = {
        "time": int(str(hours) + str(minutes)),
        "user_chat_id": call.from_user.id
    }

    if update:
        await remove_scheduler_job(call.from_user.id)

    await add_time_remind(add_data, update, call.from_user.id)
    await add_send_message(call.from_user.id, hours, minutes)
    await call.answer(
        f"Напоминание {'добавлено.' if not update else 'изменено'}",
        show_alert=True
    )
    await call.message.edit_text(
        text=menu_bot, reply_markup=main_menu, parse_mode="HTML"
    )
    await state.clear()
