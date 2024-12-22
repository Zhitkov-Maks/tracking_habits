from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from api.get_habit import (
    get_list_habits,
    get_full_info,
    archive_habit
)
from config import BOT_TOKEN
from keyboards.archive import generate_inline_habits_list
from keyboards.detail import gen_habit_keyword
from keyboards.keyboard import main_menu, confirm
from states.add import HabitState
from utils.habits import generate_message_answer, get_base_data_habit
from handlers.decorator_handlers import decorator_errors
from loader import mark_as_archive, archived

detail: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN)


@detail.callback_query(F.data == "show_habits")
@decorator_errors
async def output_list_habits(call: CallbackQuery, state: FSMContext) -> None:
    """Shows a list of active habits for today."""
    result: dict = await get_list_habits(call.from_user.id, is_active=1)
    keyword: InlineKeyboardMarkup = await generate_inline_habits_list(
        result.get("data")
    )

    await state.set_state(HabitState.show)
    await call.message.answer(
        text="Список ваших актуальных привычек",
        reply_markup=keyword
    )


@detail.callback_query(HabitState.show, F.data.isdigit())
@decorator_errors
async def detail_info_habit(call: CallbackQuery, state: FSMContext) -> None:
    """Shows detailed information about the habit."""
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)

    title, body, days = await get_base_data_habit(response)
    await state.update_data(
        id=call.data, title=title, body=body, number_of_days=days
    )
    await state.set_state(HabitState.action)

    keyword: InlineKeyboardMarkup = await gen_habit_keyword()
    await call.message.answer(
        text=text, parse_mode="HTML", reply_markup=keyword
    )


@detail.callback_query(HabitState.action, F.data == "archive")
async def habit_to_archive_confirm(call: CallbackQuery) -> None:
    """Confirmation of adding a habit to the archive."""
    await call.message.answer(text=mark_as_archive, reply_markup=confirm)


@detail.callback_query(HabitState.action, F.data == "yes")
@decorator_errors
async def habit_to_archive(call: CallbackQuery, state: FSMContext) -> None:
    """Adding a habit to the archive."""
    data: dict = await state.get_data()
    await archive_habit(int(data.get("id")), call.from_user.id, is_active=False)
    await call.message.answer(text=archived, reply_markup=main_menu)
    await state.clear()
