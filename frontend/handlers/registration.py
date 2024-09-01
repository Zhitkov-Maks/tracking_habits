from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from frontend.api.auth import registration, login_user
from frontend.config import BOT_TOKEN
from frontend.keyboards.keyboard import main_menu, cancel
from frontend.states.register import RegisterState
from frontend.utils.register import create_data

register_route = Router()
bot = Bot(token=BOT_TOKEN)


@register_route.callback_query(F.data == "registration")
async def handler_register(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(RegisterState.password)
    await call.message.answer(
        "Для регистрации будет использоваться ваш аккаунт от "
        "телеграм, поэтому вам остается придумать только пароль. Пароль "
        "должен содержать не менее 4 символов.\n<b>Введите ваш пароль:</b>",
        parse_mode="HTML",
        reply_markup=cancel
    )


@register_route.message(RegisterState.password)
async def handler_register_password(
    message: types.Message,
    state: FSMContext
) -> None:
    data: dict = await create_data(message)
    try:
        await registration(data), await login_user(data, message.from_user.id)
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAPLZsuKEwhHOtn4gpepPXZduXa"
                    "jXPcAAq8MAAJ549hIUM9aLUMN9Tw1BA"
        )

        await message.answer(
            "Ok! Вы успешно зарегистрировались! Теперь вы имеете доступ "
            "к остальному функционалу бота.",
            reply_markup=main_menu
        )

    except ClientError as err:
        await message.answer(
            text=str(err),
            reply_markup=main_menu
        )
    await state.clear()
