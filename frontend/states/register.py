from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    """Класс состояний для Регистрации."""
    password = State()
