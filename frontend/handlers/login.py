from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from api.auth import login_user
from config import BOT_TOKEN
from keyboards.keyboard import main_menu, cancel
from states.login import LoginState
from utils.register import create_data

auth = Router()
bot = Bot(token=BOT_TOKEN)


@auth.callback_query(F.data == "login")
async def handler_register(
    call: CallbackQuery,
    state: FSMContext
):
    """Спрашивает пароль для аутентификации."""
    await state.set_state(LoginState.password)
    await call.message.answer(
        text="<b>Введите ваш пароль:</b>",
        parse_mode="HTML",
        reply_markup=cancel
    )


@auth.message(LoginState.password)
async def handler_login_password(
    message: types.Message,
    state: FSMContext
) -> None:
    """Аутентифицирует пользователя."""
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
