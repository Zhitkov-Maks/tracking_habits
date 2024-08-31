from aiogram.fsm.state import StatesGroup, State


class AddState(StatesGroup):
    title = State()
    describe = State()

