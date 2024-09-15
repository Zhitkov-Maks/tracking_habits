from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from frontend.api.auth import login_user
from frontend.config import BOT_TOKEN
from frontend.keyboards.keyboard import main_menu, cancel
from frontend.states.login import LoginState
from frontend.utils.register import create_data

auth = Router()
bot = Bot(token=BOT_TOKEN)


@auth.callback_query(F.data == "login")
async def handler_register(
    call: CallbackQuery,
    state: FSMContext
):
    await state.set_state(LoginState.password)
    await call.message.answer(
        "Для входа будет также использоваться ваш аккаунт от "
        "телеграм, поэтому вам остается только ввести пароль."
        "\n<b>Введите ваш пароль:</b>",
        parse_mode="HTML",
        reply_markup=cancel
    )


@auth.message(LoginState.password)
async def handler_login_password(
    message: types.Message,
    state: FSMContext
) -> None:
    data: dict = await create_data(message)

    try:
        await login_user(data, message.from_user.id)
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAPeZsuLfu_BUoCPbpPHsfkhqXiHX8AAAtMJAAIZju"
                    "BIuwGABG11kjg1BA"
        )
        await message.answer(
            "Ok! Вы успешно вошли в ваш аккаунт! Теперь вы имеете доступ "
            "к остальному функционалу бота.",
            reply_markup=main_menu
        )

    except ClientError as err:
        await message.answer(
            text=str(err),
            reply_markup=main_menu
        )
    await state.clear()
