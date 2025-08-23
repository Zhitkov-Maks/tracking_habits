from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from api.get_habit import (
    archive_habit,
    delete_habit,
    get_full_info,
    get_list_habits
)
from keyboards.archive import (
    gen_habit_keyword_archive,
    generate_inline_habits_list
)
from keyboards.keyboard import confirm, main_menu
from loader import (
    archive_list,
    delete_habit_message,
    not_archive_list,
    recovery_text,
    success_remove,
)
from states.archive import ArchiveState
from utils.common import append_to_session, decorator_errors
from utils.habits import generate_message_answer

arch: Router = Router()


@arch.callback_query(F.data == "show_archive")
@decorator_errors
async def archive_list_habits(call: CallbackQuery, state: FSMContext) -> None:
    """Shows archived habits"""
    page: int = (await state.get_data()).get("page", 1)
    result: dict = await get_list_habits(
        call.from_user.id, page=page, is_active=0
    )
    keyword: InlineKeyboardMarkup = \
        await generate_inline_habits_list(result.get("data", []), page=page)

    if len(result.get("data", [])) != 0:
        text: str = archive_list
    else:
        text: str = not_archive_list

    await state.update_data(page=page, is_active=0)
    await state.set_state(ArchiveState.show)
    send_message = await call.message.answer(
        text=text,
        reply_markup=keyword,
        parse_mode="HTML"
    )
    await append_to_session(call.from_user.id, [call, send_message])


@arch.callback_query(ArchiveState.show, F.data.isdigit())
@decorator_errors
async def detail_info_habit(call: CallbackQuery, state: FSMContext) -> None:
    """Show detailed information about the habit from the archive."""
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)

    await state.update_data(id=call.data)
    await state.set_state(ArchiveState.action)
    keyword: InlineKeyboardMarkup = await gen_habit_keyword_archive()
    send_message = await call.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyword
    )
    await append_to_session(call.from_user.id, [call, send_message])


@arch.callback_query(ArchiveState.action, F.data == "delete")
@decorator_errors
async def delete_habit_by_id(
    call: CallbackQuery, state: FSMContext
) -> None:
    """
    Confirmation of the habit deletion. Shows the keyboard
    with the choice is yes or no.
    """
    send_message = await call.message.answer(
        text=delete_habit_message,
        reply_markup=confirm,
        parse_mode="HTML"
    )
    await append_to_session(call.from_user.id, [call, send_message])


@arch.callback_query(ArchiveState.action, F.data == "yes")
@decorator_errors
async def confirm_delete_habit_by_id(
    call: CallbackQuery, state: FSMContext
) -> None:
    """Confirmation of permanent removal of the habit."""
    data: dict = await state.get_data()
    await delete_habit(int(data.get("id", 0)), call.from_user.id)
    send_message = await call.message.answer(
        text=success_remove,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await state.clear()
    await append_to_session(call.from_user.id, [call, send_message])


@arch.callback_query(ArchiveState.action, F.data == "un_archive")
@decorator_errors
async def habit_to_un_archive(call: CallbackQuery, state: FSMContext) -> None:
    """Returning a habit from the archive for tracking."""
    data: dict = await state.get_data()
    await archive_habit(
        int(data.get("id", 0)),
        call.from_user.id,
        is_active=True
    )
    send_message = await call.message.answer(
        text=recovery_text,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await state.clear()
    await append_to_session(call.from_user.id, [call, send_message])
