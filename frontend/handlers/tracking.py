from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from frontend.api.tracking import habit_tracking_mark, \
    habit_tracking_mark_update
from frontend.keyboards.keyboard import main_menu, confirm
from frontend.states.add import HabitState
from frontend.utils.habits import inline_choice_calendar, get_choice_date, \
    inline_done_not_done, gen_message_done_not_done

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
    F.data.in_(["today", "yesterday", "beforeYesterday"])
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
async def mark_tracking_habit(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.update_data(done=call.data)
    data = await state.get_data()
    try:
        await habit_tracking_mark(
            data,
            call.from_user.id
        )
        await call.message.answer(
            text=await gen_message_done_not_done(data),
            reply_markup=main_menu,
            parse_mode="HTML"
        )
        await state.clear()
    except ClientError as err:
        await state.set_state(HabitState.confirm)
        await call.message.answer(
            text=str(err) + f"Хотите изменить запись?",
            reply_markup=confirm
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
        await call.message.answer(
            text=await gen_message_done_not_done(data),
            reply_markup=main_menu,
            parse_mode="HTML"
        )

    except (ClientError, KeyError) as err:
        await call.message.answer(
            text=str(err),
            reply_markup=main_menu
        )

    finally:
        await state.clear()
