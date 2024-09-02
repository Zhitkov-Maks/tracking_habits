from aiogram.fsm.state import StatesGroup, State


class ArchiveState(StatesGroup):
    show = State()
    action = State()
