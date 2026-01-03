from aiogram import Router, F
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboard import confirm

from api.comment import (
    get_list_comment,
    request_for_save_comment,
    delete_comment
)
from keyboards.comment import get_comment_keyboard, comment_button
from utils.comment import generate_message_answer
from utils.common import bot_send_message, decorator_errors
from loader import input_comment, is_not_valid_comment
from states.comment import CommentState


comment_router = Router()


@comment_router.callback_query(F.data == "show_comments")
@decorator_errors
async def show_comments(
    callback: CallbackQuery, state: FSMContext
) -> None:
    data: dict = await state.get_data()
    habit_id: int = data.get("id")
    result: dict[str, list[dict]] = await get_list_comment(
        callback.from_user.id,
        habit_id,
        page=1
    )
    mess, another_page, _id = await generate_message_answer(result)
    await state.update_data(page_comment=1, comment_id=_id)
    keyboard: InlineKeyboardMarkup = await get_comment_keyboard(
        another_page, page=1, comment_id=_id
    )
    await callback.message.edit_text(
        text=hbold(mess),
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@comment_router.callback_query(F.data.in_(["next_comment", "prev_comment"]))
@decorator_errors
async def next_output_list_comments(
    call: CallbackQuery, state: FSMContext
) -> None:
    """Shows a list of active habits for today."""
    data = await state.get_data()
    page: int = data.get("page_comment")
    habit_id = data.get("id")

    if call.data == "next_comment":
        page += 1
    else:
        page -= 1

    result: dict = await get_list_comment(
        call.from_user.id,
        habit_id,
        page=page
    )
    mess, another_page, _id = await generate_message_answer(result)
    keyboard: InlineKeyboardMarkup = await get_comment_keyboard(
        another_page, page=page, comment_id=_id
    )
    await state.update_data(page_comment=page, comment_id=_id)
    await call.message.edit_text(
        text=hbold(mess),
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@comment_router.callback_query(F.data == "create_comment")
async def create_comment_by_habit(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(CommentState.body)
    await callback.message.edit_text(
        text=input_comment,
        parse_mode="HTML",
        reply_markup=comment_button
    )


@comment_router.message(CommentState.body)
@decorator_errors
async def save_comment(message: Message, state: FSMContext) -> None:
    if len(message.text) < 5:
        await message.answer(
            text=is_not_valid_comment,
            parse_mode="HTML",
            reply_markup=comment_button
        )
    else:
        data: dict = await state.get_data()
        habit_id: int = data.get("id")
        await request_for_save_comment(
            message.from_user.id,
            habit_id,
            {"body": message.text}
        )
        await bot_send_message(state, message.from_user.id)


@comment_router.callback_query(F.data == "remove_comment")
@decorator_errors
async def remove_comment_by_id(
    call: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(CommentState.confirm)
    await call.message.edit_text(
        text=hbold("Подтвердите удаление."),
        parse_mode="HTML",
        reply_markup=confirm
    )


@comment_router.callback_query(CommentState.confirm)
@decorator_errors
async def confirm_remove_comment(
    call: CallbackQuery, state: FSMContext
) -> None:
    data = await state.get_data()
    comment_id: int = data.get("comment_id")
    await delete_comment(comment_id, call.from_user.id)
    await bot_send_message(state, call.from_user.id)
