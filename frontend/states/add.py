from aiogram.fsm.state import StatesGroup, State


class AddState(StatesGroup):
    title = State()
    describe = State()
    numbers_of_days = State()


class HabitState(StatesGroup):
    show = State()
    action = State()
    date = State()
    done = State()
    confirm = State()


class EditState(StatesGroup):
    title = State()
    describe = State()
    numbers_of_days = State()
