from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from frontend.api.remind import add_time_remind, remove_time
from frontend.keyboards.keyboard import (
    remind_button,
    main_menu,
    confirm
)

from frontend.states.remind import RemindState
from frontend.utils.remind import create_time, add_send_message

remind = Router()


@remind.callback_query(F.data == "remind")
async def start_work_to_remind(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(RemindState.start)
    await call.message.answer(
        text="Выберите действие",
        reply_markup=remind_button
    )


@remind.callback_query(RemindState.start, F.data == "remove")
async def confirm_to_remove_remind(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(RemindState.confirm)
    await call.message.answer(
        text="Вы уверены?",
        reply_markup=confirm
    )


@remind.callback_query(RemindState.confirm, F.data == "yes")
async def finalize_remove(
    call: CallbackQuery,

) -> None:
    try:
        await remove_time(call.from_user.id)
        await call.message.answer(
            text="Напоминание было удалено.",
            reply_markup=main_menu
        )
    except (ClientError, KeyError) as err:
        await call.message.answer(
            text=str(err),
            reply_markup=main_menu
        )


@remind.callback_query(RemindState.start, F.data.in_(["add", "change"]))
async def add_remind(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(RemindState.add)
    if call.data == "change":
        await state.update_data(update=True)
    else:
        await state.update_data(update=False)
    await call.message.answer(
        text="Выберите в какой час вам напомнить о "
             "необходимости сделать запись.",
        reply_markup=await create_time()
    )


@remind.callback_query(RemindState.add, F.data.isdigit())
async def finalize_add_remind(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    update: bool = (await state.get_data())["update"]
    data: dict = {"time": int(call.data)}
    try:
        await add_time_remind(data, update, call.from_user.id)
        await add_send_message(call.from_user.id, time=int(call.data))
        await call.message.answer(
            text=f"Напоминание {'добавлено.' if not update else 'изменено'}",
            reply_markup=main_menu
        )
    except (ClientError, KeyError) as err:
        await call.message.answer(
            text=str(err),
            reply_markup=main_menu
        )
