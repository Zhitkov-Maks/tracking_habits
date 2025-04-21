from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from api.remind import add_time_remind, remove_time
from handlers.decorator_handlers import decorator_errors
from keyboards.keyboard import (
    remind_button,
    main_menu,
    confirm
)
from keyboards.remind import create_time

from states.remind import RemindState
from utils.remind import (
    add_send_message,
    remove_scheduler_job
)
from loader import menu_remind, choice_hour

remind: Router = Router()


@remind.callback_query(F.data == "remind")
async def start_work_to_remind(call: CallbackQuery, state: FSMContext) -> None:
    """
    A command handler for working with reminders.
    Shows a menu for selecting an action.
    """
    await state.set_state(RemindState.start)
    await call.message.edit_text(
        text=menu_remind, reply_markup=remind_button
    )


@remind.callback_query(RemindState.start, F.data == "remove")
async def confirm_to_remove_remind(
        call: CallbackQuery, state: FSMContext
) -> None:
    """
    The handler of the command to delete the reminder.
    Shows the menu for confirmation.
    """
    await state.set_state(RemindState.confirm)
    await call.message.edit_text(text="Вы уверены?", reply_markup=confirm)


@remind.callback_query(RemindState.confirm, F.data == "yes")
@decorator_errors
async def finalize_remove(call: CallbackQuery, state: FSMContext) -> None:
    """The handler for deleting the reminder."""
    await remove_time(call.from_user.id)
    await remove_scheduler_job(call.from_user.id)
    await call.answer(text="Напоминание удалено", show_alert=True)
    await call.message.edit_text(
        text="Меню!", reply_markup=main_menu
    )
    await state.clear()


@remind.callback_query(RemindState.start, F.data.in_(["add", "change"]))
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

    await call.message.edit_text(
        text=choice_hour,
        reply_markup=await create_time()
    )


@remind.callback_query(RemindState.add, F.data.isdigit())
@decorator_errors
async def finalize_add_remind(call: CallbackQuery, state: FSMContext) -> None:
    """The final handler for adding a reminder."""
    update: bool = (await state.get_data())["update"]
    data: dict = {"time": int(call.data), "user_chat_id": call.from_user.id}

    if update:
        await remove_scheduler_job(call.from_user.id)

    await add_time_remind(data, update, call.from_user.id)
    await add_send_message(call.from_user.id, time=int(call.data))
    await call.answer(
        f"Напоминание {'добавлено.' if not update else 'изменено'}",
        show_alert=True
    )
    await call.message.answer(text="Меню", reply_markup=main_menu)
    await state.clear()
