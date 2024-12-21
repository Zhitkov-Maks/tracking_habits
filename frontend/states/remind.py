from aiogram.fsm.state import StatesGroup, State


class RemindState(StatesGroup):
    """A status class for reminders."""
    start = State()
    add = State()
    confirm = State()
