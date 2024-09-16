from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from api.exeptions import DateValidationError
from api.get import get_full_info
from api.tracking import (
    habit_tracking_mark,
    habit_tracking_mark_update
)
from keyboards.keyboard import main_menu, confirm
from states.add import HabitState
from utils.habits import (
    inline_choice_calendar,
    get_choice_date,
    inline_done_not_done,
    days_ago,
    generate_message_answer,
    gen_habit_keyword
)

track = Router()


@track.callback_query(HabitState.action, F.data == "mark")
async def choice_date(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    keyword = await inline_choice_calendar()
    await state.set_state(HabitState.done)
    await call.message.answer(
        text="Выберите вариант. Более поздних дат не предусмотрено, так "
             "как если вы не отмечали два дня скорее всего вы не "
             "выполняли условие, поэтому стоит начать сначала, "
             "выбрав вариант под привычкой очистить.",
        reply_markup=keyword
    )


@track.callback_query(
    HabitState.done,
    F.data.in_(days_ago)
)
async def choice_done(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    date: str = await get_choice_date(call.data)
    keyword = await inline_done_not_done()
    await state.update_data(date=date)
    await state.set_state(HabitState.date)
    await call.message.answer(
        text="Выберите выполнено/не выполнено",
        reply_markup=keyword
    )


@track.callback_query(
    HabitState.date,
    F.data.in_(["done", "not_done"])
)
async def mark_tracking_habit_done(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.update_data(done=call.data)
    data: dict = await state.get_data()
    try:
        await habit_tracking_mark(
            data,
            call.from_user.id
        )
        response: dict = await get_full_info(data.get("id"), call.from_user.id)
        await state.set_state(HabitState.action)

        await call.message.answer(
            text=await generate_message_answer(response),
            parse_mode="HTML",
            reply_markup=await gen_habit_keyword()
        )

    except ClientError as err:
        await state.set_state(HabitState.confirm)
        await call.message.answer(
            text=str(err) + f"Хотите изменить запись?",
            reply_markup=confirm
        )

    except DateValidationError as err:
        response: dict = await get_full_info(data.get("id"), call.from_user.id)
        await state.set_state(HabitState.action)
        await call.message.answer(text=str(err))
        await call.message.answer(
            text=await generate_message_answer(response),
            parse_mode="HTML",
            reply_markup=await gen_habit_keyword()
        )


@track.callback_query(HabitState.confirm, F.data == "yes")
async def mark_tracking_habit_update(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    data: dict = await state.get_data()
    try:
        await habit_tracking_mark_update(
            data,
            call.from_user.id
        )
        response: dict = await get_full_info(data.get("id"), call.from_user.id)
        await state.set_state(HabitState.action)
        await call.message.answer(
            text=await generate_message_answer(response),
            parse_mode="HTML",
            reply_markup=await gen_habit_keyword()
        )

    except (ClientError, KeyError) as err:
        await call.message.answer(
            text=str(err),
            reply_markup=main_menu
        )
