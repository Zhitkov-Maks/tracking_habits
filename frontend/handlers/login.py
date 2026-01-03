import asyncio
from typing import Dict
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from api.auth import login_user
from api.reset import revoke_token
from config import WORKER_BOT
from keyboards.keyboard import cancel, main_menu
from keyboards.reset import generate_inline_keyboard_reset
from loader import (
    enter_email,
    invalid_email,
    invalid_pass,
    password,
    success_auth,
    clear_history
)
from states.login import LoginState
from utils.common import (
    decorator_errors,
    remove_message_after_delay,
    delete_jwt_token,
    send_sticker
)
from utils.register import create_data, is_valid_email, is_valid_password

auth = Router()

STICKERS_LIST = [
    "cheburator.tgs",
    "hello.tgs",
    "hi_cat.tgs",
    "hi_croco.tgs",
    "hi_fire.tgs",
    "hI_hi.tgs",
    "hi_windows.tgs",
    "HI.tgs"
]


@auth.message(F.text == "/auth")
@decorator_errors
async def input_email(mess: Message, state: FSMContext) -> None:
    """The handler for the email request."""
    await state.set_state(LoginState.email)
    await mess.answer(
        text=enter_email, parse_mode="HTML", reply_markup=cancel
    )


@auth.callback_query(F.data == "auth")
@decorator_errors
async def input_email_callback(
    call: CallbackQuery, state: FSMContext
) -> None:
    """The handler for the email request."""
    await state.set_state(LoginState.email)
    await call.message.edit_text(
        text=enter_email, parse_mode="HTML", reply_markup=cancel
    )


@auth.message(LoginState.email)
@decorator_errors
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
        await mess.answer(
            text=text + enter_email,
            parse_mode="HTML",
            reply_markup=cancel
        )


@auth.message(LoginState.password)
@decorator_errors
async def final_authentication(message: Message, state: FSMContext) -> None:
    """The handler authenticates the user."""
    valid: bool = is_valid_password(message.text)
    asyncio.create_task(remove_message_after_delay(5, message))

    if valid:
        email: str = (await state.get_data())["email"]
        data: Dict[str, str] = await create_data(email, message.text)
        result: str | None = await login_user(data, message.from_user.id)
        if result is None:
            await send_sticker(
                message.from_user.id,
                random.choice(STICKERS_LIST)
            )
            await message.answer(
                success_auth,
                reply_markup=main_menu,
                parse_mode="HTML"
            )
            await state.clear()
        else:
            await message.answer(
                result + ". Попробуйте еще раз.",
                reply_markup=await generate_inline_keyboard_reset(),
                parse_mode="HTML"
            )
            await state.set_state(LoginState.email)

    else:
        text: str = invalid_pass
        await message.answer(
            text=text + password, parse_mode="HTML", reply_markup=cancel
        )


@auth.callback_query(F.data == "clear_history")
@decorator_errors
async def clean_messages(
    callback: CallbackQuery,
    state: FSMContext
):
    """
    Clears the message history,
    revokes the token, and deletes the saved token.
    """
    user_id = callback.from_user.id
    await revoke_token(user_id)
    await delete_jwt_token(user_id)
    await WORKER_BOT.send_message(
        chat_id=user_id,
        text=hbold(clear_history),
        reply_markup=main_menu,
        parse_mode="HTML"
    )
