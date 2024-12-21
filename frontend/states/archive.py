from aiogram.fsm.state import StatesGroup, State


class ArchiveState(StatesGroup):
    """A class of states for working with the archive."""
    show = State()
    action = State()
