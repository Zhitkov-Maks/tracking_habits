from aiogram.fsm.state import StatesGroup, State


class LoginState(StatesGroup):
    """Класс состояний для авторизации."""
    password = State()
