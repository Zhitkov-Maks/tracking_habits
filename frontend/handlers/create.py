from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiohttp import ClientError

from frontend.api.create import request_create_habit
from frontend.keyboards.keyboard import cancel, main_menu
from frontend.states.add import AddState

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
        parse_mode=ParseMode.HTML,
        reply_markup=cancel
    )


@add.message(AddState.describe)
async def create_and_record_db(
        mess: Message,
        state: FSMContext
) -> None:
    await state.update_data(body=mess.text)
    await state.set_state(AddState.numbers_of_days)
    await mess.answer(
        text="Сколько дней будем отслеживать?",
        reply_markup=cancel
    )


@add.message(AddState.numbers_of_days, F.text.isdigit())
async def create_and_record_db(
        mess: Message,
        state: FSMContext
) -> None:
    await state.update_data(number_of_days=mess.text)
    try:
        await request_create_habit(
            await state.get_data(), mess.from_user.id
        )
        await mess.answer(
            text="Ваша привычка успешно сохранена. Не забывайте "
                 "ежедневно выполнять ее и добавлять в отслеживание.",
            reply_markup=main_menu
        )
    except (ClientError, KeyError) as err:
        await mess.answer(
            text=str(err),
            reply_markup=main_menu
        )
    await state.clear()


@add.message(AddState.numbers_of_days)
async def handler_errors(mess: Message):
    await mess.answer(
        text="Ошибка ввода, нужно было ввести число, попробуйте сначала.",
        reply_markup=main_menu
    )