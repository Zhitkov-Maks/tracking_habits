from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from frontend.api.get import (
    get_full_info,
    delete_habit,
    get_list_habits,
    archive_habit
)
from frontend.keyboards.keyboard import main_menu
from frontend.states.archive import ArchiveState
from frontend.utils.archive import gen_habit_keyword_archive
from frontend.utils.habits import (
    generate_inline_habits_list,
    generate_message_answer
)

arch = Router()


@arch.callback_query(F.data == "show_archive")
async def archive_list_habits(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    try:
        result: dict = await get_list_habits(
            call.from_user.id, is_active=0
        )
        keyword = await generate_inline_habits_list(result.get("data"))
        await state.set_state(ArchiveState.show)
        await call.message.answer(
            text="Список ваших привычек из архива.",
            reply_markup=keyword
        )
    except (ClientError, KeyError) as err:
        await call.message.answer(
            text=str(err),
            reply_markup=main_menu
        )


@arch.callback_query(ArchiveState.show)
async def detail_info_habit(
    call: CallbackQuery,
    state: FSMContext
):
    response: dict = await get_full_info(int(call.data), call.from_user.id)
    text: str = await generate_message_answer(response)
    await state.update_data(id=call.data)
    await state.set_state(ArchiveState.action)
    keyword = await gen_habit_keyword_archive()

    await call.message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyword
    )


@arch.callback_query(ArchiveState.action, F.data == "delete")
async def delete_habit_by_id(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    data = await state.get_data()
    try:
        await delete_habit(int(data.get("id")), call.from_user.id)
        await call.message.answer(
            text="Привычка была удалена, без возможности восстановления.",
            reply_markup=main_menu
        )
    except (ClientError, KeyError) as err:
        await call.message.answer(str(err))

    finally:
        await state.clear()


@arch.callback_query(ArchiveState.action, F.data == "un_archive")
async def habit_to_un_archive(
    call: CallbackQuery,
    state: FSMContext
) -> None:
    data = await state.get_data()
    try:
        await archive_habit(
            int(data.get("id")), call.from_user.id, is_active=True
        )
        await call.message.answer(
            text="Привычка была помечена как активная и будет "
                 "отображаться в списке активных привычек..",
            reply_markup=main_menu
        )
    except (ClientError, KeyError) as err:
        await call.message.answer(str(err))

    finally:
        await state.clear()
