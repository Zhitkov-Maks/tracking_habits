from aiogram.fsm.state import StatesGroup, State


class LoginState(StatesGroup):
    password = State()
