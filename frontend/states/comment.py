from aiogram.fsm.state import StatesGroup, State


class CommentState(StatesGroup):
    """A class of states for adding comments."""
    body = State()
    confirm = State()
