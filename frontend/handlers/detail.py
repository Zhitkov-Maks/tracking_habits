from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from frontend.api.get import (
    get_list_habits,
    get_full_info,
    delete_habit,
    archive_habit
)
from frontend.api.tracking import habit_clean_all_tracking
from frontend.config import BOT_TOKEN
from frontend.keyboards.keyboard import main_menu
from frontend.states.add import HabitState
from frontend.utils.habits import generate_inline_habits_list, \
    generate_message_answer, gen_habit_keyword

detail = Router()
bot = Bot(token=BOT_TOKEN)


@detail.callback_query(F.data == "show_habits")
async def output_list_habits(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    try:
        result: dict = await get_list_habits(
            call.from_user.id
        )
        keyword = await generate_inline_habits_list(result.get("data"))
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


@detail.callback_query(HabitState.show)
async def detail_info_habit(
    call: CallbackQuery,
    state: FSMContext
):
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)
    await state.update_data(id=call.data)
    await state.set_state(HabitState.action)
    keyword = await gen_habit_keyword()

    await call.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyword
    )


@detail.callback_query(HabitState.action, F.data == "clean")
async def delete_habit_by_id(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    data = await state.get_data()
    try:
        await habit_clean_all_tracking(int(data.get("id")), call.from_user.id)
        await call.message.answer(
            text="Все отметки о выполнении были удалены.",
            reply_markup=main_menu
        )
        await state.clear()
    except (ClientError, KeyError) as err:
        await state.clear()
        await call.message.answer(str(err))


@detail.callback_query(HabitState.action, F.data == "delete")
async def delete_habit_by_id(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    data = await state.get_data()
    try:
        await delete_habit(int(data.get("id")), call.from_user.id)
        await call.message.answer(
            text="Привычка была удалена.",
            reply_markup=main_menu
        )
        await state.clear()
    except (ClientError, KeyError) as err:
        await state.clear()
        await call.message.answer(str(err))


@detail.callback_query(HabitState.action, F.data == "archive")
async def habit_to_archive(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    data = await state.get_data()
    try:
        await archive_habit(int(data.get("id")), call.from_user.id)
        await call.message.answer(
            text="Привычка была помечена как выполнена и не будет "
                 "отображаться в списке активных привычек..",
            reply_markup=main_menu
        )
        await state.clear()
    except (ClientError, KeyError) as err:
        await state.clear()
        await call.message.answer(str(err))
