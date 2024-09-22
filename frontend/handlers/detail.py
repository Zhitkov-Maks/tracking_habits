from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiohttp import ClientError

from api.get import (
    get_list_habits,
    get_full_info,
    archive_habit
)
from config import BOT_TOKEN
from keyboards.keyboard import main_menu, confirm
from states.add import HabitState
from utils.habits import generate_inline_habits_list, \
    generate_message_answer, gen_habit_keyword

detail = Router()
bot = Bot(token=BOT_TOKEN)


@detail.callback_query(F.data == "show_habits")
async def output_list_habits(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    """Обработчик для показа отслеживаемых привычек."""
    try:
        result: dict = await get_list_habits(
            call.from_user.id, is_active=1
        )
        keyword: InlineKeyboardMarkup = \
            await generate_inline_habits_list(result.get("data"))

        await state.set_state(HabitState.show)
        await call.message.answer(
            text="Список ваших актуальных привычек",
            reply_markup=keyword
        )
    except (ClientError, KeyError) as err:
        await call.message.answer(
            text=str(err),
            reply_markup=main_menu
        )


@detail.callback_query(HabitState.show, F.data.isdigit())
async def detail_info_habit(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    """Показывает подробную информацию о привычке."""
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)

    await state.update_data(id=call.data)
    await state.set_state(HabitState.action)
    keyword: InlineKeyboardMarkup = await gen_habit_keyword()

    await call.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyword
    )


@detail.callback_query(HabitState.action, F.data == "archive")
async def habit_to_archive_confirm(
    call: CallbackQuery,
) -> None:
    """Подтверждение добавления привычки в архив."""
    await call.message.answer(
        text="Привычка будет помечена как архивная и не будет отображаться "
             "в активных привычках"
             "Нажмите да чтобы продолжить или нет чтобы отменить действие.",
        reply_markup=confirm
    )


@detail.callback_query(HabitState.action, F.data == "yes")
async def habit_to_archive(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    """Добавление привычки в архив."""
    data: dict = await state.get_data()
    try:
        await archive_habit(
            int(data.get("id")), call.from_user.id, is_active=False
        )
        await call.message.answer(
            text="Привычка была помечена как выполнена и не будет "
                 "отображаться в списке активных привычек..",
            reply_markup=main_menu
        )
        await state.clear()
    except (ClientError, KeyError) as err:
        await state.clear()
        await call.message.answer(str(err))
