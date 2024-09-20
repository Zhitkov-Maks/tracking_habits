from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from api.auth import registration, login_user
from config import BOT_TOKEN
from keyboards.keyboard import main_menu, cancel
from states.register import RegisterState
from utils.register import create_data

register_route = Router()
bot = Bot(token=BOT_TOKEN)


@register_route.callback_query(F.data == "registration")
async def handler_register(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    """Обработчик для запроса пароля."""
    await state.set_state(RegisterState.password)
    await call.message.answer(
        text="<b>Придумайте ваш пароль(не менее 5 символов).</b>",
        parse_mode="HTML",
        reply_markup=cancel
    )


@register_route.message(RegisterState.password)
async def handler_register_password(
    message: types.Message,
    state: FSMContext
) -> None:
    """Создает и аутентифицирует пользователя."""
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
