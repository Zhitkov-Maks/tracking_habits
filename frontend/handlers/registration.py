import asyncio
from typing import Dict

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api.auth import registration, login_user
from config import BOT_TOKEN
from loader import (
    enter_email,
    password,
    success_registration,
    invalid_email,
    invalid_pass
)
from keyboards.keyboard import main_menu, cancel
from states.register import RegisterState
from utils.register import create_data, is_valid_email, is_valid_password
from utils.common import (
    remove_message_after_delay,
    append_to_session,
    decorator_errors
)


register_route = Router()
bot = Bot(token=BOT_TOKEN)


@register_route.message(F.text == "/register")
@decorator_errors
async def input_email(mess: Message, state: FSMContext) -> None:
    """The handler for the email request."""
    await state.set_state(RegisterState.email)
    send_message = await mess.answer(
        text=enter_email,
        parse_mode="HTML",
        reply_markup=cancel
    )
    await append_to_session(mess.from_user.id, [mess, send_message])


@register_route.message(RegisterState.email)
@decorator_errors
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
        send_message = await mess.answer(
            text=password, parse_mode="HTML", reply_markup=cancel
        )
    else:
        send_message = await mess.answer(
            text=invalid_email + enter_email,
            parse_mode="HTML", reply_markup=cancel
        )
    await append_to_session(mess.from_user.id, [send_message])


@register_route.message(RegisterState.password)
@decorator_errors
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
            send_message = await message.answer(
                success_registration,
                reply_markup=main_menu,
                parse_mode="HTML"
            )
        else:
            send_message = await message.answer(result, reply_markup=main_menu)
        await state.clear()

    else:
        send_message = await message.answer(
            text=invalid_pass + password,
            parse_mode="HTML", reply_markup=cancel
        )
    await append_to_session(message.from_user.id, [send_message])
