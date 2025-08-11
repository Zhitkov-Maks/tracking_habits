import asyncio
from typing import Dict

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from api.auth import login_user
from config import BOT_TOKEN
from keyboards.keyboard import cancel, main_menu
from keyboards.reset import generate_inline_keyboard_reset
from loader import (
    enter_email,
    invalid_email,
    invalid_pass,
    password,
    success_auth
)
from states.login import LoginState
from utils.common import (
    append_to_session,
    delete_sessions,
    remove_message_after_delay,
    delete_jwt_token
)
from utils.register import create_data, is_valid_email, is_valid_password

auth = Router()
bot = Bot(token=BOT_TOKEN)


@auth.message(F.text == "/auth")
async def input_email(mess: Message, state: FSMContext) -> None:
    """The handler for the email request."""
    await state.set_state(LoginState.email)
    send_message = await mess.answer(
        text=enter_email,
        parse_mode="HTML",
        reply_markup=cancel
    )
    await append_to_session(mess.from_user.id, [mess, send_message])


@auth.message(LoginState.email)
async def input_password(mess: Message, state: FSMContext) -> None:
    """The handler for the password request."""
    valid: bool = is_valid_email(mess.text)
    asyncio.create_task(remove_message_after_delay(5, mess))

    if valid:
        await state.update_data(email=mess.text)
        await state.set_state(LoginState.password)
        send_message = await mess.answer(
            text=password, parse_mode="HTML", reply_markup=cancel
        )

    else:
        text: str = invalid_email
        send_message = await mess.answer(
            text=text + enter_email,
            parse_mode="HTML",
            reply_markup=cancel
        )
    await append_to_session(mess.from_user.id, [send_message])


@auth.message(LoginState.password)
async def final_authentication(message: Message, state: FSMContext) -> None:
    """The handler authenticates the user."""
    valid: bool = is_valid_password(message.text)
    asyncio.create_task(remove_message_after_delay(5, message))

    if valid:
        email: str = (await state.get_data())["email"]
        data: Dict[str, str] = await create_data(email, message.text)
        result: str | None = await login_user(data, message.from_user.id)
        if result is None:
            send_message = await message.answer(
                success_auth,
                reply_markup=main_menu,
                parse_mode="HTML"
            )
        else:
            send_message = await message.answer(
                result, reply_markup=await generate_inline_keyboard_reset()
            )
        await state.clear()

    else:
        text: str = invalid_pass
        send_message = await message.answer(
            text=text + password, parse_mode="HTML", reply_markup=cancel
        )
    await append_to_session(message.from_user.id, [send_message])


@auth.callback_query(F.data == "clear_history")
async def clean_messages(callback: CallbackQuery):
    await delete_sessions(callback.from_user.id)
    await delete_jwt_token(callback.from_user.id)
