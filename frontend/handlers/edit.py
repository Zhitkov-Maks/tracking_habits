from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiohttp import ClientError
from aiogram import F

from api.edit import request_update_habit
from keyboards.keyboard import cancel, main_menu
from states.add import EditState, HabitState

edit_rout = Router()


@edit_rout.callback_query(HabitState.action, F.data == "edit")
async def edit_habit_title(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(EditState.title)
    text = hbold("1-й этап") + ("\nДайте название привычке которую вы "
                                "хотите отслеживать: ")
    await call.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@edit_rout.message(EditState.title)
async def edit_description_habit(
    mess: Message,
    state: FSMContext
) -> None:
    await state.update_data(title=mess.text)
    await state.set_state(EditState.describe)
    await mess.answer(
        text=hbold("2-й этап") + "\nВведите новое описание привычки :",
        parse_mode=ParseMode.HTML,
        reply_markup=cancel
    )


@edit_rout.message(EditState.describe)
async def edit_habit_number_of_days(
    mess: Message,
    state: FSMContext
) -> None:
    await state.update_data(body=mess.text)
    await state.set_state(EditState.numbers_of_days)
    await mess.answer(
        text="Сколько дней будем отслеживать?",
        reply_markup=cancel
    )


@edit_rout.message(EditState.numbers_of_days, F.text.isdigit())
async def create_and_record_db(
    mess: Message,
    state: FSMContext
) -> None:
    await state.update_data(number_of_days=mess.text)
    try:
        await request_update_habit(
            await state.get_data(), mess.from_user.id
        )
        await mess.answer(
            text="Ваша привычка успешно обновлена. Не забывайте "
                 "ежедневно выполнять ее и добавлять в отслеживание.",
            reply_markup=main_menu
        )
    except (ClientError, KeyError) as err:
        await mess.answer(
            text=str(err),
            reply_markup=main_menu
        )
    await state.clear()
