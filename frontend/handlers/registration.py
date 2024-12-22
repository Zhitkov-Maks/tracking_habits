import asyncio
from typing import Dict

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.auth import registration, login_user
from config import BOT_TOKEN
from loader import enter_email, password, success_registration
from keyboards.keyboard import main_menu, cancel
from states.register import RegisterState
from utils.register import create_data, is_valid_email, is_valid_password
from utils.common import remove_message_after_delay


register_route = Router()
bot = Bot(token=BOT_TOKEN)


@register_route.message(F.text == "/register")
async def input_email(mess: Message, state: FSMContext) -> None:
    """The handler for the email request."""
    await state.set_state(RegisterState.email)
    await mess.answer(text=enter_email, parse_mode="HTML", reply_markup=cancel)


@register_route.message(RegisterState.email)
async def input_password(
    mess: Message,
    state: FSMContext
) -> None:
    """The handler for the password request."""
    valid: bool = is_valid_email(mess.text)
    asyncio.create_task(remove_message_after_delay(5, mess))
    if valid:
        await state.update_data(email=mess.text)
        await state.set_state(RegisterState.password)
        await mess.answer(
            text=password, parse_mode="HTML", reply_markup=cancel
        )
    else:
        text: str = "Ваш email не соответствует требованиям! "
        await mess.answer(
            text=text + enter_email, parse_mode="HTML", reply_markup=cancel
        )


@register_route.message(RegisterState.password)
async def final_registration(
    message: Message,
    state: FSMContext
) -> None:
    """The handler Creates and authenticates the user."""
    valid: bool = is_valid_password(message.text)
    asyncio.create_task(remove_message_after_delay(5, message))

    if valid:
        email: str = (await state.get_data())["email"]
        data: Dict[str, str] = await create_data(email, message.text)
        result: str | None = await registration(data)

        # If the request is successful, None will be returned to us
        if result is None:
            await login_user(data, message.from_user.id)
            await message.answer(success_registration, reply_markup=main_menu)
        else:
            await message.answer(result, reply_markup=main_menu)

    else:
        text: str = "Ваш пароль не соответствует требованиям! "
        await message.answer(
            text=text + password, parse_mode="HTML", reply_markup=cancel
        )
