from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from api.get_habit import archive_habit, get_full_info, get_list_habits
from keyboards.archive import generate_inline_habits_list
from keyboards.detail import gen_habit_keyboard
from keyboards.keyboard import confirm, main_menu
from loader import active_list, archived, mark_as_archive, not_active_list
from states.add import HabitState
from states.archive import ArchiveState
from utils.common import append_to_session, decorator_errors
from utils.habits import generate_message_answer, get_base_data_habit

detail: Router = Router()


@detail.callback_query(F.data == "show_habits")
@decorator_errors
async def output_list_habits(call: CallbackQuery, state: FSMContext) -> None:
    """Shows a list of active habits for today."""
    page: int = (await state.get_data()).get("page", 1)
    result: dict[str, list] = await get_list_habits(
        call.from_user.id, page=page, is_active=1
    )

    keyword: InlineKeyboardMarkup = await generate_inline_habits_list(
        result.get("data", []), page=page
    )

    if len(result.get("data", [])) != 0:
        text: str = active_list
    else:
        text: str = not_active_list

    await state.update_data(page=page, is_active=1)
    await state.set_state(HabitState.show)
    send_message = await call.message.edit_text(
        text=text,
        reply_markup=keyword,
        parse_mode="HTML"
    )
    await append_to_session(call.from_user.id, [call, send_message])


@detail.callback_query(F.data.in_(["next_page", "prev_page"]))
@decorator_errors
async def next_output_list_habits(
    call: CallbackQuery, state: FSMContext
) -> None:
    """Shows a list of active habits for today."""
    page: int = (await state.get_data()).get("page")
    is_active: int = (await state.get_data()).get("is_active")

    if call.data == "next_page":
        page += 1
    else:
        page -= 1

    result: dict = await get_list_habits(
        call.from_user.id, page=page, is_active=is_active
    )
    keyword: InlineKeyboardMarkup = await generate_inline_habits_list(
        result.get("data", []), page
    )
    await state.update_data(page=page)

    if is_active:
        await state.set_state(HabitState.show)
    else:
        await state.set_state(ArchiveState.show)

    send_message = await call.message.edit_reply_markup(
        reply_markup=keyword
    )
    await append_to_session(call.from_user.id, [call, send_message])


@detail.callback_query(HabitState.show, F.data.isdigit())
@decorator_errors
async def detail_info_habit(call: CallbackQuery, state: FSMContext) -> None:
    """Shows detailed information about the habit."""
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)
    title, body, days = await get_base_data_habit(response)
    await state.update_data(
        id=call.data,
        title=title,
        body=body,
        number_of_days=days
    )
    await state.set_state(HabitState.action)

    keyword: InlineKeyboardMarkup = await gen_habit_keyboard()
    send_message = await call.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyword
    )
    await append_to_session(call.from_user.id, [call, send_message])


@detail.callback_query(F.data == "show_detail")
@decorator_errors
async def show_detail_habit(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_: int = data.get("id")
    response: dict = await get_full_info(id_, call.from_user.id)
    text: str = await generate_message_answer(response)
    keyboard: InlineKeyboardMarkup = await gen_habit_keyboard()

    await state.set_state(HabitState.action)
    send_message = await call.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await append_to_session(call.from_user.id, [call, send_message])


@detail.callback_query(HabitState.action, F.data == "archive")
@decorator_errors
async def habit_to_archive_confirm(
    call: CallbackQuery, state: FSMContext
) -> None:
    """Confirmation of adding a habit to the archive."""
    send_message = await call.message.answer(
        text=mark_as_archive,
        reply_markup=confirm,
        parse_mode="HTML"
    )
    await append_to_session(call.from_user.id, [call, send_message])


@detail.callback_query(HabitState.action, F.data == "yes")
@decorator_errors
async def habit_to_archive(call: CallbackQuery, state: FSMContext) -> None:
    """Adding a habit to the archive."""
    data: dict = await state.get_data()
    await archive_habit(
        int(data.get("id", 0)),
        call.from_user.id, is_active=False
    )
    send_message = await call.message.edit_text(
        text=archived,
        reply_markup=main_menu,
        parse_mode="HTML"
    )
    await state.clear()
    await append_to_session(call.from_user.id, [call, send_message])
