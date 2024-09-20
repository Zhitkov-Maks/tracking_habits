from aiogram.fsm.state import StatesGroup, State


class ArchiveState(StatesGroup):
    """Класс состояний для работы с архивом."""
    show = State()
    action = State()
