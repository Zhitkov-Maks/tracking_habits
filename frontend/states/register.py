from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    password = State()
