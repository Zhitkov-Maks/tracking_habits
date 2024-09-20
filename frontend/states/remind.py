from aiogram.fsm.state import StatesGroup, State


class RemindState(StatesGroup):
    """Класс состояний для напоминаний."""
    start = State()
    add = State()
    confirm = State()
