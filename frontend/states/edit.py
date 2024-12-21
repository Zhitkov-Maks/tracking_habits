from aiogram.fsm.state import StatesGroup, State


class FullEditState(StatesGroup):
    """A class of states for editing habits."""
    title = State()
    describe = State()
    numbers_of_days = State()


class PartialEditHabit(StatesGroup):
    """A class of states for partial habit editing."""
    title: State = State()
    body: State = State()
    number_of_days: State = State()
    save: State = State()
