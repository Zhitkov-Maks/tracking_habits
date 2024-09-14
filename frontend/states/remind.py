from aiogram.fsm.state import StatesGroup, State


class RemindState(StatesGroup):
    start = State()
    choice = State()
    confirm = State()