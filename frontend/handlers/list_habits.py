from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from frontend.api.list_habits import get_list_habits
from frontend.keyboards.keyboard import cancel, main_menu
from frontend.states.add import AddState
from frontend.api.add_habit import *

add = Router()


@add.callback_query(F.data == "show_habits")
async def output_list_habits(
    call: CallbackQuery
) -> None:
    result: list = await get_list_habits(
        call.from_user.id
    )
    for i in result:
        await call.message.answer(i)
