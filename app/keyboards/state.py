from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    update_text = State()

    add_event = State()
    add_social = State()