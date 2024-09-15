from aiogram.fsm.state import StatesGroup, State


class RemindState(StatesGroup):
    start = State()
    add = State()
    confirm = State()
