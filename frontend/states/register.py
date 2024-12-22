from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    """The class of states to Register."""
    email: State = State()
    password: State = State()
