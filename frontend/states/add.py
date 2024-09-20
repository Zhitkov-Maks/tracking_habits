from aiogram.fsm.state import StatesGroup, State


class AddState(StatesGroup):
    """Класс состояний для добавления привычки."""
    title = State()
    describe = State()
    numbers_of_days = State()


class HabitState(StatesGroup):
    """Класс состояний для работы с привычкой."""
    show = State()
    action = State()
    date = State()
    done = State()
    confirm = State()


class EditState(StatesGroup):
    """Класс состояний для редактирования привычки."""
    title = State()
    describe = State()
    numbers_of_days = State()
