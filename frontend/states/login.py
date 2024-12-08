from aiogram.fsm.state import StatesGroup, State


class LoginState(StatesGroup):
    """The class of states to Authorisation."""
    email: State = State()
    password: State = State()
