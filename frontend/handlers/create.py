from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode

from api.create import request_create_habit
from keyboards.keyboard import cancel, main_menu
from states.add import AddState

add: Router = Router()


@add.callback_query(F.data == "create")
async def input_name_habits(call: CallbackQuery, state: FSMContext) -> None:
    """The handler asks the user for the name of the habit."""
    text: str = hbold("1-й этап") + (
        "\nВведите краткое название привычки которую вы хотите отследить..."
    )
    await state.set_state(AddState.title)
    await call.message.answer(
        text=text, parse_mode="HTML", reply_markup=cancel
    )


@add.message(AddState.title)
async def input_describe_habits(mess: Message, state: FSMContext) -> None:
    """The handler asks the user for a description of the habit."""
    await state.update_data(title=mess.text)
    await state.set_state(AddState.describe)
    await mess.answer(
        text=hbold("2-й этап") + (
            "\nОпишите подробнее о привычке и цели которую вы хотите достичь..."),
        parse_mode=ParseMode.HTML,
        reply_markup=cancel
    )


@add.message(AddState.describe)
async def input_numbers_days(mess: Message, state: FSMContext) -> None:
    """The handler asks the user for the number of days to track."""
    await state.update_data(body=mess.text)
    await state.set_state(AddState.numbers_of_days)
    await mess.answer(
        text=hbold("3-й этап\n") + "Сколько дней будем отслеживать?",
        reply_markup=cancel,
        parse_mode="HTML"
    )


@add.message(AddState.numbers_of_days, F.text.isdigit())
async def create_and_record_db(mess: Message, state: FSMContext) -> None:
    """The handler sends all the entered data for saving.."""
    await state.update_data(number_of_days=mess.text)
    try:
        result: None | str = await request_create_habit(
            await state.get_data(), mess.from_user.id
        )
        if result is None:
            text: str = ("Ваша привычка успешно сохранена. Не забывайте "
                         "ежедневно выполнять ее и добавлять в отслеживание.")
        else:
            text: str = result
        await mess.answer(text=text, reply_markup=main_menu)

    except KeyError as err:
        await mess.answer(text=str(err), reply_markup=main_menu)
    await state.clear()


@add.message(AddState.numbers_of_days)
async def handler_errors(mess: Message) -> None:
    """Handler if the user suddenly entered a string instead of a number."""
    await mess.answer(
        text="Ошибка ввода, нужно было ввести число, попробуйте сначала.",
        reply_markup=main_menu
    )
