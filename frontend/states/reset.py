from aiogram.fsm.state import StatesGroup, State


class ResetPassword(StatesGroup):
    send_email: State = State()
    send_token: State = State()