from aiogram.fsm.state import StatesGroup, State


class AddState(StatesGroup):
    title = State()
    describe = State()
    numbers_of_days = State()


