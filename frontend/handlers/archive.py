from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from api.get_habit import (
    get_full_info,
    delete_habit,
    get_list_habits,
    archive_habit
)
from loader import delete_habit_message
from handlers.decorator_handlers import decorator_errors
from keyboards.archive import (
    generate_inline_habits_list,
    gen_habit_keyword_archive
)
from keyboards.keyboard import main_menu, confirm
from states.archive import ArchiveState
from utils.habits import generate_message_answer

arch: Router = Router()


@arch.callback_query(F.data == "show_archive")
@decorator_errors
async def archive_list_habits(call: CallbackQuery, state: FSMContext) -> None:
    """Shows archived habits"""
    result: dict = await get_list_habits(call.from_user.id, is_active=0)
    keyword: InlineKeyboardMarkup = \
        await generate_inline_habits_list(result.get("data"))

    if len(result.get("data")) != 0:
        text: str = "Список ваших привычек из архива."
    else:
        text: str = "У вас нет архивированных привычек."

    await state.set_state(ArchiveState.show)
    await call.message.answer(text=text, reply_markup=keyword)


@arch.callback_query(ArchiveState.show)
@decorator_errors
async def detail_info_habit(call: CallbackQuery, state: FSMContext) -> None:
    """Show detailed information about the habit from the archive."""
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)

    await state.update_data(id=call.data)
    await state.set_state(ArchiveState.action)

    keyword: InlineKeyboardMarkup = await gen_habit_keyword_archive()
    await call.message.answer(
        text=text, parse_mode="HTML", reply_markup=keyword
    )


@arch.callback_query(ArchiveState.action, F.data == "delete")
async def delete_habit_by_id(call: CallbackQuery) -> None:
    """
    Confirmation of the habit deletion. Shows the keyboard
    with the choice is yes or no.
    """
    await call.message.answer(text=delete_habit_message, reply_markup=confirm)


@arch.callback_query(ArchiveState.action, F.data == "yes")
@decorator_errors
async def delete_habit_by_id(call: CallbackQuery, state: FSMContext) -> None:
    """Confirmation of permanent removal of the habit."""
    data: dict = await state.get_data()
    await delete_habit(int(data.get("id")), call.from_user.id)
    await call.message.answer(
        text="Привычка была удалена, без возможности восстановления.",
        reply_markup=main_menu
    )
    await state.clear()


@arch.callback_query(ArchiveState.action, F.data == "un_archive")
@decorator_errors
async def habit_to_un_archive(call: CallbackQuery, state: FSMContext) -> None:
    """Returning a habit from the archive for tracking."""
    data: dict = await state.get_data()
    await archive_habit(int(data.get("id")), call.from_user.id, is_active=True)
    await call.message.answer(
        text="Привычка была помечена как активная и будет "
             "отображаться в списке активных привычек.",
        reply_markup=main_menu
    )
    await state.clear()
