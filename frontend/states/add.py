from aiogram.fsm.state import StatesGroup, State


class AddState(StatesGroup):
    """A class of states for adding habits."""
    title = State()
    describe = State()
    numbers_of_days = State()


class HabitState(StatesGroup):
    """A class of states for working with a habit."""
    show = State()
    action = State()
    date = State()
    done = State()
    confirm = State()
