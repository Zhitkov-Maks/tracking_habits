import asyncio
from typing import Dict

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from api.reset import get_token_for_reset, query_for_reset_password
from handlers.decorator_handlers import decorator_errors
from keyboards.keyboard import cancel, main_menu
from loader import password
from states.reset import ResetPassword
from utils.common import remove_message_after_delay
from utils.register import is_valid_email, is_valid_password

reset: Router = Router()


@reset.message(F.text == "/reset")
async def input_email_for_reset(mess: Message, state: FSMContext) -> None:
    """A function for requesting an email to reset the password."""
    await state.set_state(ResetPassword.send_email)
    await mess.answer(text="Введите email от вашего аккаунта", reply_markup=cancel)


@reset.callback_query(F.data == "reset")
async def input_email_for_reset(call: CallbackQuery, state: FSMContext) -> None:
    """A function for requesting an email to reset the password."""
    await state.set_state(ResetPassword.send_email)
    await call.message.answer(
        text="Введите email от вашего аккаунта", reply_markup=cancel
    )


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
        token: Dict[str, str] = await get_token_for_reset(email)
        await state.set_state(ResetPassword.send_token)
        await state.update_data(token=token.get("token"))
        await message.answer(
            text=hbold("Придумайте новый пароль. Пароль должен содержать "
                       "буквы и цифры и быть не короче 5 символов."),
            reply_markup=cancel, parse_mode="HTML")
    else:
        text: str = "Ваш email не соответствует требованиям! "
        await message.answer(
            text=text + email, parse_mode="HTML", reply_markup=cancel
        )


@reset.message(ResetPassword.send_token)
@decorator_errors
async def reset_password_query(message: Message, state: FSMContext) -> None:
    """Sends a new password to change the user's password."""
    new_password: str = message.text
    asyncio.create_task(remove_message_after_delay(5, message))
    is_valid: bool = is_valid_password(new_password)
    if is_valid:
        data: Dict[str, str] = await state.get_data()
        await query_for_reset_password(data.get("token"), new_password)
        await message.answer(text="Ваш пароль был успешно изменен. "
                                  "Теперь вы можете войти в свой аккаунт.",
                             reply_markup=main_menu
                             )
    else:
        text: str = "Ваш пароль не соответствует требованиям! "
        await message.answer(
            text=text + password, parse_mode="HTML", reply_markup=cancel
        )
