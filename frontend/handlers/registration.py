from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

from frontend.api.auth import registration, login_user
from frontend.config import BOT_TOKEN
from frontend.keyboards.keyboard import main_menu, cancel
from frontend.states.register import RegisterState
from frontend.utils.register import create_data

register_route = Router()
bot = Bot(token=BOT_TOKEN)


@register_route.message(F.text == "/register")
async def handler_register(message: types.Message, state: FSMContext):
    await state.set_state(RegisterState.password)
    await message.answer(
        "Для регистрации будет использоваться ваш аккаунт от "
        "телеграм, поэтому вам остается придумать только пароль. Пароль "
        "должен содержать не менее 8 символов.\n<b>Введите ваш пароль:</b>",
        parse_mode="HTML",
        reply_markup=cancel
    )


@register_route.message(RegisterState.password)
async def handler_register_password(
    message: types.Message,
    state: FSMContext
) -> None:
    data: dict = await create_data(message)
    result = await registration(data)
    login = await login_user(data, message.from_user.id)
    if isinstance(result, bool) and login:
        await bot.send_sticker(
            message.chat.id,
            sticker="CAACAgIAAxkBAAPLZsuKEwhHOtn4gpepPXZduXajXPcAAq8MAAJ549hIUM9aLUMN9Tw1BA")
        await message.answer(
            "Ok! Вы успешно зарегистрировались! Теперь вы имеете доступ "
            "к остальному функционалу бота.",
            reply_markup=main_menu
        )
    else:
        await message.answer(
            result,
            reply_markup=main_menu
        )
    await state.clear()
