from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from frontend.keyboards.keyboard import cancel, main_menu
from frontend.states.add import AddState
from frontend.api.add_habit import *

add = Router()


@add.callback_query(F.data == "create")
async def input_name_habits(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    text = hbold("1-й этап") + ("\nВведите привычку которую вы хотите "
                                "приобрести: ")
    await state.set_state(AddState.title)
    await call.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@add.message(AddState.title)
async def input_describe_habits(
    mess: Message,
    state: FSMContext
) -> None:
    await state.update_data(title=mess.text)
    await state.set_state(AddState.describe)
    await mess.answer(
        text=hbold("2-й этап") + ("\nОпишите подробнее о "
                                 "привычке и цели которую вы хотите достичь:"),
        parse_mode="HTML",
        reply_markup=cancel
    )


@add.message(AddState.describe)
async def create_and_record_db(
    mess: Message,
    state: FSMContext
) -> None:
    await state.update_data(body=mess.text)
    response: str = await request_create_habit(
        await state.get_data(), mess.from_user.id
    )
    await mess.answer(
        text=response,
        reply_markup=main_menu
    )
    await state.clear()
