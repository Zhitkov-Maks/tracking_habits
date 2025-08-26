import asyncio
from typing import Dict

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from api.reset import get_token_for_reset, query_for_reset_password
from keyboards.keyboard import cancel, main_menu
from loader import (
    password,
    enter_email,
    invalid_email,
    invalid_pass,
    success_reset,
    input_token
)
from states.reset import ResetPassword
from utils.common import (
    remove_message_after_delay,
    append_to_session,
    decorator_errors
)
from utils.register import is_valid_email, is_valid_password

reset: Router = Router()


@reset.message(F.text == "/reset")
@decorator_errors
async def input_email_for_reset(mess: Message, state: FSMContext) -> None:
    """A function for requesting an email to reset the password."""
    await state.set_state(ResetPassword.send_email)
    send_message = await mess.answer(
        text=enter_email,
        reply_markup=cancel,
        parse_mode="HTML"
    )
    await append_to_session(mess.from_user.id, [mess, send_message])


@reset.callback_query(F.data == "reset")
@decorator_errors
async def input_email_for_reset_callback(
    call: CallbackQuery, state: FSMContext
) -> None:
    """A function for requesting an email to reset the password."""
    await state.set_state(ResetPassword.send_email)
    send_message = await call.message.edit_text(
        text=enter_email,
        reply_markup=cancel,
        parse_mode="HTML"
    )
    await append_to_session(call.from_user.id, [call, send_message])


@reset.message(ResetPassword.send_email)
@decorator_errors
async def send_request_for_reset(message: Message, state: FSMContext) -> None:
    """
    Sends a request to the server, if such an email exists,
    then a token is returned for the next request,
    which is valid for 1 minute.
    """
    email: str = message.text
    asyncio.create_task(remove_message_after_delay(5, message))
    is_valid: bool = is_valid_email(email)
    if is_valid:
        await get_token_for_reset(email)
        await state.set_state(ResetPassword.send_token)
        send_message = await message.answer(
            text=input_token,
            reply_markup=cancel, parse_mode="HTML")
    else:
        send_message = await message.answer(
            text=invalid_email + email,
            parse_mode="HTML",
            reply_markup=cancel
        )
    await append_to_session(message.from_user.id, [message, send_message])
    
    
@reset.message(ResetPassword.send_token)
@decorator_errors
async def get_token(message: Message, state: FSMContext) -> None:
    """Saves the token to be sent to the server.."""
    token: str = message.text
    await state.update_data(token=token)
    await state.set_state(ResetPassword.send_password)
    asyncio.create_task(remove_message_after_delay(30, message))
    send_message = await message.answer(
            text=password,
            parse_mode="HTML",
            reply_markup=cancel
        )
    await append_to_session(message.from_user.id, [message, send_message])


@reset.message(ResetPassword.send_password)
@decorator_errors
async def reset_password_query(message: Message, state: FSMContext) -> None:
    """Sends a new password to change the user's password."""
    new_password: str = message.text
    asyncio.create_task(remove_message_after_delay(15, message))
    is_valid: bool = is_valid_password(new_password)
    if is_valid:
        data: Dict[str, str] = await state.get_data()
        await query_for_reset_password(data.get("token"), new_password)
        send_message = await message.answer(
            text=success_reset,
            reply_markup=main_menu
        )
        await state.clear()
    else:
        send_message = await message.answer(
            text=invalid_pass + password,
            parse_mode="HTML",
            reply_markup=cancel
        )
    await append_to_session(message.from_user.id, [message, send_message])
